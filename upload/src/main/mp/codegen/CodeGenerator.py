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
        intype = [ArrayPointerType(StringType())] if isMain else list()
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))

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
        return SubBody(None, [Symbol(ast.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym)

    def visitCallStmt(self, ast, o):
        #ast: CallStmt
        #o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
    
        ctype = sym.mtype

        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

    def visitVarDecl(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        env = ctxt.sym
        if frame:#param and local
            idx = frame.getNewIndex()
            self.emit.printout(self.emit.emitVAR(idx,ast.variable.name, ast.varType, frame.getStartLabel(), frame.getEndLabel(), frame))
            return SubBody(frame,[Symbol(ast.variable.name,ast.varType,Index(idx))]+env)
        else:#global var
            self.emit.printout(self.emit.emitATTRIBUTE(ast.variable.name,ast.varType,False,""))
            return SubBody(None,[Symbol(ast.variable.name,ast.varType,CName(self.className))]+env)

    def visitUnaryOp(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        opstr = ""
        op = ast.op#operator
        exp_c,exp_t = self.visit(ast.body,o)#return code and type    
        if ast.op == 'not':
            opstr = exp_c + self.emit.emitNOT(IntType(),frame)    
            restype = BoolType()
        else:
            opstr = exp_c + self.emit.emitNEGOP(exp_t,frame)
            restype = exp_t
        o = ctxt
        return opstr, restype

    def visitBinaryOp(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        opstr = ""
        op = ast.op#operator
        lc,lt = self.visit(ast.left,o)#return code and type
        rc,rt = self.visit(ast.right,o)

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
        elif ast.op == 'div':
            restype = IntType()
            opstr = lc + rc + self.emit.emitDIV(frame)
        elif ast.op == 'mod':
            restype = IntType()
            opstr = lc + rc + self.emit.emitMOD(frame)    
        elif ast.op == 'and':
            restype = BoolType()
            opstr = lc + rc + self.emit.emitANDOP(frame)
        elif ast.op == 'or':
            restype = BoolType()
            opstr = lc + rc + self.emit.emitOROP(frame)         

        return opstr,restype

    def visitAssign(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        rc,rt = self.visit(ast.exp,Access(frame,ctxt.sym,False,True))
        lc,lt = self.visit(ast.lhs,Access(frame,ctxt.sym,True,False))
        self.emit.printout(rc + lc)
        return rc + lc 

    def visitId(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        res = self.lookup(ast.name,ctxt.sym,lambda x: x.name)
        if ctxt.isLeft:
            if type(res.value) is CName:
                return self.emit.emitPUTSTATIC(res.value.value + "/" + res.name,res.mtype,frame),res.mtype
            else:
                return self.emit.emitWRITEVAR(res.name,res.mtype,res.value.value,frame),res.mtype
        else: 
            if type(res.value) is CName:
                return self.emit.emitGETSTATIC(res.value.value + "/" + res.name,res.mtype,frame),res.mtype
            else:
                return self.emit.emitREADVAR(res.name,res.mtype,res.value.value,frame),res.mtype
        
    def visitIf(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        result = list()
        # exp_c, exp_t = self.visit(ast.expr,Access(frame,ctxt.sym,False,True))
        # result.append(exp_c)#gen code for exp
        # labelE = frame.getNewLabel()
        # labelNext = frame.getNewLabel()

        # result.append(self.emit.emitIFFALSE(labelE,frame))
        # thenstmt = [self.visit(x,o) for x in ast.thenStmt]
        # thenstmt=''.join(str(x) for x in thenstmt)
        # result.append(thenstmt)
        # result.append(self.emit.emitGOTO(labelNext,frame))
        # result.append(self.emit.emitLABEL(labelE,frame))
        # elsestmt = [self.visit(x,o) for x in ast.elseStmt]
        # elsestmt = ''.join(str(x) for x in elsestmt)
        # result.append(elsestmt)
        # result.append(self.emit.emitLABEL(labelNext,frame))
        exp_c, exp_t = self.visit(ast.expr,Access(frame,ctxt.sym,False,True))
        result.append(exp_c)#gen code for exp
        self.emit.printout(result[-1])
        labelE = frame.getNewLabel()
        labelNext = frame.getNewLabel()

        if ast.elseStmt != []:
            lab = labelE
        else: 
            lab = labelNext
        result.append(self.emit.emitIFFALSE(lab,frame))
        self.emit.printout(result[-1])
        thenstmt = [self.visit(x,o) for x in ast.thenStmt]
        thenstmt = ''.join(str(x) for x in thenstmt)
        result.append(thenstmt)
        if ast.elseStmt != None:
            result.append(self.emit.emitGOTO(labelNext,frame))
            self.emit.printout(result[-1])
            result.append(self.emit.emitLABEL(labelE,frame))
            self.emit.printout(result[-1])
            elsestmt = [self.visit(x,o) for x in ast.elseStmt]
            elsestmt = ''.join(str(x) for x in elsestmt)
            result.append(elsestmt)
        result.append(self.emit.emitLABEL(labelNext,frame))
        self.emit.printout(result[-1])
        code = ''.join(result)

        return code

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
