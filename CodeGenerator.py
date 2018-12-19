'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [    Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
                    Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("getFloat", MType([], FloatType()), CName(self.libName)),
                    Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("putBool", MType([BoolType()], VoidType()), CName(self.libName)),
                    Symbol("putBoolLn", MType([BoolType()], VoidType()), CName(self.libName)),
                    Symbol("putString", MType([StringType()], VoidType()), CName(self.libName)),
                    Symbol("putStringLn", MType([StringType()], VoidType()), CName(self.libName)),
                    Symbol("putLn", MType([], VoidType()), CName(self.libName)),
                    ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

# class StringType(Type):
    
#     def __str__(self):
#         return "StringType"

#     def accept(self, v, param):
#         return None

class ArrayPointerType(Type):
    def __init__(self, ctype):
        #cname: String
        self.eleType = ctype

    def __str__(self):
        return "ArrayPointerType({0})".format(str(self.eleType))

    def accept(self, v, param):
        return None
class ClassType(Type):
    def __init__(self,cname):
        self.cname = cname
    def __str__(self):
        return "Class({0})".format(str(self.cname))
    def accept(self, v, param):
        return None
        
class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym

class Access():
    def __init__(self, frame, sym, isLeft, isFirst):
        #frame: Frame
        #sym: List[Symbol]
        #isLeft: Boolean
        #isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value

class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File

        self.astTree = astTree
        self.env = env
        self.className = "MPClass"
        self.path = dir_
        self.emit = Emitter(self.path + "/" + self.className + ".j")

    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any

        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        e = SubBody(None, self.env)
        for x in ast.decl:
            e = self.visit(x, e)
        # generate default constructor
        self.genMETHOD(FuncDecl(Id("<init>"), list(), list(), list(),None), c, Frame("<init>", VoidType))
        self.emit.emitEPILOG()
        return c

    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame

        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayPointerType(StringType())] if isMain else [x.varType for x in consdecl.param]
        mtype = MType(intype, returnType)

        if isInit:
            self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))
        else:
            self.emit.printout(self.emit.emitMETHOD(methodName, mtype, True, frame))

        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations and local
        param = consdecl.param
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        else:
            if param:
                subbody = SubBody(frame, glenv)
                for x in param:
                    subbody = self.visit(x,subbody)
                frame = subbody.frame
                glenv = subbody.sym

        
        local = consdecl.local
        if local:
            subbody = SubBody(frame, glenv)
            for x in local:
                subbody = self.visit(x,subbody)
            frame = subbody.frame
            glenv = subbody.sym

        body = consdecl.body
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        #print(frame.getEndLabel())

        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def visitFuncDecl(self, ast, o):
        #ast: FuncDecl
        #o: Any

        subctxt = o
        frame = Frame(ast.name, ast.returnType)
        self.genMETHOD(ast, subctxt.sym, frame)
        return SubBody(None, [Symbol(ast.name.name, MType([x.varType for x in ast.param], ast.returnType), CName(self.className))] + subctxt.sym)

    def visitCallStmt(self, ast, o):
        #ast: CallStmt
        #o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
    
        ctype = sym.mtype
        inputtyp = None
        if type(ctype) is MType:
            inputtyp = ctype.partype
        in_ = ("", list())
        i = 0
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            if inputtyp:
                if type(inputtyp[i]) is FloatType and type(typ1) is IntType:
                    str1 = str1 + self.emit.emitI2F(frame)
            in_ = (in_[0] + str1, list())
            i = i + 1
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

    def visitCallExpr(self, ast, o): 
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
    
        ctype = sym.mtype
        inputtyp = None
        if type(ctype) is MType:
            inputtyp = ctype.partype
        in_ = ("", list())
        i = 0
        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            if inputtyp:
                if type(inputtyp[i]) is FloatType and type(typ1) is IntType:
                    str1 = str1 + self.emit.emitI2F(frame)
            in_ = (in_[0] + str1, list())
            i = i + 1

        return in_[0] + self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame),ctype

    def visitVarDecl(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        env = ctxt.sym
        if frame:#param and local
            idx = frame.getNewIndex()
            self.emit.printout(self.emit.emitVAR(idx,ast.variable.name.lower(), ast.varType, frame.getStartLabel(), frame.getEndLabel(), frame))
            return SubBody(frame,[Symbol(ast.variable.name.lower(),ast.varType,Index(idx))]+env)
        else:#global var
            self.emit.printout(self.emit.emitATTRIBUTE(ast.variable.name.lower(),ast.varType,False,""))
            return SubBody(None,[Symbol(ast.variable.name.lower(),ast.varType,CName(self.className))]+env)

    def visitUnaryOp(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        opstr = ""
        op = ast.op#operator
        exp_c,exp_t = self.visit(ast.body,o)#return code and type    
        if ast.op.lower() == 'not':
            opstr = exp_c + self.emit.emitNOT(IntType(),frame)    
            restype = BoolType()
        else:
            opstr = exp_c + self.emit.emitNEGOP(exp_t,frame)
            restype = exp_t

        return opstr, restype

    def visitBinaryOp(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        opstr = ""
        op = ast.op#operator
        lc,lt = self.visit(ast.left,o)#return code and type
        rc,rt = self.visit(ast.right,o)
        restype = IntType()
        if ast.op in ['+','-']:
            if type(lt) is IntType and type(rt) is FloatType:
                opstr = lc + self.emit.emitI2F(frame) + rc + self.emit.emitADDOP(op, FloatType(), frame)
                restype = FloatType()
            elif type(lt) is FloatType and type(rt) is IntType:
                opstr = lc + rc + self.emit.emitI2F(frame) + self.emit.emitADDOP(op, FloatType(), frame)
                restype = FloatType()
            else:
                opstr = lc + rc + self.emit.emitADDOP(op, lt, frame)
                restype = lt
        elif ast.op == '*':
            if type(lt) is IntType and type(rt) is FloatType:
                opstr = lc + self.emit.emitI2F(frame) + rc + self.emit.emitMULOP(op, FloatType(), frame)
                restype = FloatType()
            elif type(lt) is FloatType and type(rt) is IntType:
                opstr = lc + rc + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
                restype = FloatType()
            else:
                opstr = lc + rc + self.emit.emitMULOP(op, lt, frame)    
                restype = lt
        elif ast.op == '/':
            if type(lt) is IntType and type(rt) is FloatType:
                opstr = lc + self.emit.emitI2F(frame) + rc + self.emit.emitMULOP(op, FloatType(), frame)
                restype = FloatType()
            elif type(lt) is FloatType and type(rt) is IntType:
                opstr = lc + rc + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
                restype = FloatType()
            elif type(lt) is IntType and type(rt) is IntType:
                opstr = lc + self.emit.emitI2F(frame) + rc + self.emit.emitI2F(frame) + self.emit.emitMULOP(op, FloatType(), frame)
                restype = FloatType()
            else:
                opstr = lc + rc + self.emit.emitMULOP(op, lt, frame)  
                restype = lt
        elif ast.op in ['<','<=','>=','>']:
            restype = BoolType()
            if type(lt) is IntType and type(rt) is FloatType:
                opstr = lc + self.emit.emitI2F(frame) + rc + self.emit.emitREFOP(op, FloatType(), frame)
            elif type(lt) is FloatType and type(rt) is IntType:
                opstr = lc + rc + self.emit.emitI2F(frame) + self.emit.emitREFOP(op, FloatType(), frame)
            elif type(lt) is FloatType:
                opstr = lc + rc + self.emit.emitREFOP(op, lt, frame)
            else:
                opstr = lc + rc + self.emit.emitREOP(op, lt, frame)                
        elif ast.op in ['=','<>']:
            restype = BoolType()
            if type(lt) is IntType and type(rt) is IntType:
                opstr = lc + rc + self.emit.emitREOP(op, IntType(), frame)
            elif type(lt) is BoolType and type(rt) is BoolType:
                opstr = lc + rc + self.emit.emitREOP(op, BoolType(), frame)   
            elif type(lt) is FloatType and type(rt) is IntType:
                opstr = lc + rc + self.emit.emitI2F(frame) + self.emit.emitREFOP(op, FloatType(), frame) 
            elif type(lt) is IntType and type(rt) is FloatType:
                opstr = lc + self.emit.emitI2F(frame) + rc + self.emit.emitREFOP(op, FloatType(), frame) 
        elif ast.op.lower() in 'div':
            restype = IntType()
            opstr = lc + rc + self.emit.emitDIV(frame)
        elif ast.op.lower() == 'mod':
            restype = IntType()
            opstr = lc + rc + self.emit.emitMOD(frame)    
        elif ast.op.lower() == 'and':
            restype = BoolType()
            opstr = lc + rc + self.emit.emitANDOP(frame)
        elif ast.op.lower() == 'or':
            restype = BoolType()
            opstr = lc + rc + self.emit.emitOROP(frame)         
        elif ast.op.lower() == 'orelse':
            restype = BoolType()
            labelN = frame.getNewLabel()
            labelE = frame.getNewLabel()
            labelTer = frame.getNewLabel()
            isFalse1 = self.emit.emitIFFALSE(labelN,frame)
            isFalse2 = self.emit.emitIFFALSE(labelE,frame)
            resTrue = self.emit.emitPUSHCONST("1", IntType(), frame)
            resFalse = self.emit.emitPUSHCONST("0", IntType(), frame)
            NLab = self.emit.emitLABEL(labelN,frame)#next label 
            falseLab = self.emit.emitLABEL(labelE,frame)
            endLab = self.emit.emitLABEL(labelTer,frame)
            goEnd = self.emit.emitGOTO(labelTer,frame)
            opstr = lc + isFalse1 + resTrue + goEnd + NLab + rc + isFalse2 + resTrue + goEnd +  falseLab + resFalse + endLab
            
        elif ast.op.lower() == 'andthen':
            restype = BoolType()
            labelN = frame.getNewLabel()
            labelE = frame.getNewLabel()
            labelTer = frame.getNewLabel()
            isTrue1 = self.emit.emitIFTRUE(labelN,frame)
            isTrue2 = self.emit.emitIFTRUE(labelE,frame)
            resTrue = self.emit.emitPUSHCONST("1", IntType(), frame)
            resFalse = self.emit.emitPUSHCONST("0", IntType(), frame)
            NLab = self.emit.emitLABEL(labelN,frame)#next label 
            TrueLab = self.emit.emitLABEL(labelE,frame)
            endLab = self.emit.emitLABEL(labelTer,frame)
            goEnd = self.emit.emitGOTO(labelTer,frame)
            opstr = lc + isTrue1 + resFalse + goEnd + NLab + rc + isTrue2 + resFalse + goEnd +  TrueLab + resTrue + endLab
        
        return opstr,restype

    def visitAssign(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        rc,rt = self.visit(ast.exp,Access(frame,ctxt.sym,False,True))
        lc,lt = self.visit(ast.lhs,Access(frame,ctxt.sym,True,False))
        if type(lt) is FloatType and type(rt) is IntType:
            self.emit.printout(rc + self.emit.emitI2F(frame) + lc)
        else:
            self.emit.printout(rc + lc)
        return rc + lc 

    def visitId(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        res = self.lookup(ast.name.lower(),ctxt.sym,lambda x: x.name)
        if res:
            if ctxt.isLeft:
                if type(res.value) is CName:
                    return self.emit.emitPUTSTATIC(res.value.value + "/" + res.name.lower(),res.mtype,frame),res.mtype
                else:
                    return self.emit.emitWRITEVAR(res.name.lower(),res.mtype,res.value.value,frame),res.mtype
            else: 
                if type(res.value) is CName:
                    return self.emit.emitGETSTATIC(res.value.value + "/" + res.name.lower(),res.mtype,frame),res.mtype
                else:
                    # print(str(res.name))
                    # print(str(res.mtype))
                    return self.emit.emitREADVAR(res.name.lower(),res.mtype,res.value.value,frame),res.mtype
            
    def visitIf(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        exp_c, exp_t = self.visit(ast.expr,Access(frame,ctxt.sym,False,True))
        self.emit.printout(exp_c)#gen code for exp

        if len(ast.elseStmt) != 0:
            labelE = frame.getNewLabel()
            self.emit.printout(self.emit.emitIFFALSE(labelE,frame))
        else:
            labelNext = frame.getNewLabel()
            self.emit.printout(self.emit.emitIFFALSE(labelNext,frame))
        thenstmt = [self.visit(x,o) for x in ast.thenStmt]
        elsestmt = [False]
        if len(ast.elseStmt) != 0:
            labelNext = frame.getNewLabel()
            self.emit.printout(self.emit.emitGOTO(labelNext,frame))
            self.emit.printout(self.emit.emitLABEL(labelE,frame))
            elsestmt = [self.visit(x,o) for x in ast.elseStmt]
            self.emit.printout(self.emit.emitLABEL(labelNext,frame))
        else:
            self.emit.printout(self.emit.emitLABEL(labelNext,frame))
        if True in thenstmt and True in elsestmt:
            self.emit.printout(self.emit.emitRETURN(VoidType(),frame))
            return True



    def visitWhile(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        frame.enterLoop()
        breakLab = frame.getBreakLabel()
        conLab = frame.getContinueLabel()
        self.emit.printout(self.emit.emitLABEL(conLab,frame))
        exp_c, exp_t = self.visit(ast.exp,Access(frame,ctxt.sym,False,True))
        self.emit.printout(exp_c)
        self.emit.printout(self.emit.emitIFFALSE(breakLab,frame))
        dostmt = [self.visit(x,o) for x in ast.sl]
        self.emit.printout(self.emit.emitGOTO(conLab,frame))
        self.emit.printout(self.emit.emitLABEL(breakLab,frame))
        frame.exitLoop()

    def visitFor(self,ast,o):
        ctxt = o
        frame = ctxt.frame

        label0 = frame.getNewLabel()
        exp1_c, exp1_t = self.visit(ast.expr1,Access(frame,ctxt.sym,False,True))
        exp2_c, exp2_t = self.visit(ast.expr2,Access(frame,ctxt.sym,False,True))
        IdL_c, IdL_t = self.visit(ast.id,Access(frame,ctxt.sym,True,False))
        IdR_c, IdR_t = self.visit(ast.id,Access(frame,ctxt.sym,False,True))  
        self.emit.printout(exp1_c + IdL_c)
        self.emit.printout(IdR_c)
        self.emit.printout(self.emit.emitPUSHICONST(1,frame))
        if ast.up:
            self.emit.printout(self.emit.emitADDOP('-',IntType(),frame))
        else:
            self.emit.printout(self.emit.emitADDOP('+',IntType(),frame))
        self.emit.printout(IdL_c)  
        frame.enterLoop()
        conLab = frame.getContinueLabel()
        breakLab = frame.getBreakLabel()
        self.emit.printout(self.emit.emitLABEL(conLab,frame))  
        self.emit.printout(IdR_c)  
        self.emit.printout(self.emit.emitPUSHICONST(1,frame))
        if ast.up:
            self.emit.printout(self.emit.emitADDOP('+',IntType(),frame))
        else:
            self.emit.printout(self.emit.emitADDOP('-',IntType(),frame))
        self.emit.printout(IdL_c)  
  
        self.emit.printout(IdR_c + exp2_c)  
        if ast.up:
            self.emit.printout(self.emit.emitIFICMPGT(breakLab,frame))
        else:
            self.emit.printout(self.emit.emitIFICMPLT(breakLab,frame))            
        dostmt = [self.visit(x,ctxt) for x in ast.loop]
        self.emit.printout(self.emit.emitGOTO(conLab,frame))
        self.emit.printout(self.emit.emitLABEL(breakLab,frame))
        frame.exitLoop()


    def visitWith(self, ast, o):
        ctxt = o
        frame = ctxt.frame

        frame.enterScope(False)
        subbody = SubBody(frame,ctxt.sym)
        for x in ast.decl:
            subbody = self.visit(x,subbody)

        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))   
        list(map(lambda x: self.visit(x,subbody), ast.stmt))
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        frame.exitScope()

    def visitBreak(self, ast, o):
        frame = o.frame
        breakLab = frame.getBreakLabel() 
        self.emit.printout(self.emit.emitGOTO(breakLab,frame))

    def visitContinue(self,ast,o):
        frame = o.frame
        conLab = frame.getContinueLabel()
        self.emit.printout(self.emit.emitGOTO(conLab,frame))

    def visitReturn(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        exp_c = str()
        if ast.expr:
            exp_c,exp_t = self.visit(ast.expr,Access(frame,ctxt.sym,False,True))
            if type(exp_t) is IntType and type(frame.returnType) is FloatType:
                res = exp_c + self.emit.emitI2F(frame) + self.emit.emitRETURN(FloatType(),frame)
            else:
                res = exp_c + self.emit.emitRETURN(exp_t,frame)
            self.emit.printout(res)
        return True



    def visitIntLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any

        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(ast.value, frame), IntType()

    def visitFloatLiteral(self, ast, o):
        #ast: FloatLiteral
        #o: Any

        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHFCONST(str(ast.value), frame), FloatType()
    
    def visitBooleanLiteral(self,ast,o):
        #ast: BoolLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(str(ast.value).lower(), frame), BoolType()
    
    def visitStringLiteral(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHCONST('"' + ast.value + '"',StringType(),frame),StringType()
