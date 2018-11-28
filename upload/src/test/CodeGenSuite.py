import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):

    def test_int_ast0(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putInt"),[IntLiteral(5)])])])
    	expect = "5"
    	self.assertTrue(TestCodeGen.test(input,expect,500))


    def test_float_ast1(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putFloatLn"),[FloatLiteral(5.5)])])])
    	expect = "5.5\n"
    	self.assertTrue(TestCodeGen.test(input,expect,501))

    def test_bool_ast2(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBool"),[BooleanLiteral(False)])])])
    	expect = "false"
    	self.assertTrue(TestCodeGen.test(input,expect,502))

    def test_string_ast3(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putString"),[StringLiteral("Thao")])])])
    	expect = "Thao"
    	self.assertTrue(TestCodeGen.test(input,expect,503))
    
    def test_addop_int4(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putIntLn"),[BinaryOp('+',IntLiteral(1),IntLiteral(4))]),
                CallStmt(Id("putInt"),[BinaryOp('-',IntLiteral(1),IntLiteral(4))]),])])
    	expect = "5\n-3"
    	self.assertTrue(TestCodeGen.test(input,expect,504))        

    def test_mulop_int5(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putInt"),[BinaryOp('*',IntLiteral(1),IntLiteral(4))])])])
    	expect = "4"
    	self.assertTrue(TestCodeGen.test(input,expect,505))  

    def test_addop_int_float6(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putFloatLn"),[BinaryOp('+',IntLiteral(1),FloatLiteral(4.5))]),
                CallStmt(Id("putFloatLn"),[BinaryOp('-',IntLiteral(1),FloatLiteral(4.5))]),
                CallStmt(Id("putFloatLn"),[BinaryOp('+',FloatLiteral(5.5),IntLiteral(2))]),
                CallStmt(Id("putFloat"),[BinaryOp('-',FloatLiteral(5.5),IntLiteral(2))])])])
    	expect = "5.5\n-3.5\n7.5\n3.5"
    	self.assertTrue(TestCodeGen.test(input,expect,506))

    def test_addop_float7(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putFloatLn"),[BinaryOp('+',FloatLiteral(1.0),FloatLiteral(4.5))]),
                CallStmt(Id("putFloat"),[BinaryOp('-',FloatLiteral(1.0),FloatLiteral(4.5))])])])
    	expect = "5.5\n-3.5"
    	self.assertTrue(TestCodeGen.test(input,expect,507))

    def test_mulop_int8(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putFloatLn"),[BinaryOp('*',IntLiteral(2),FloatLiteral(4.5))]),
                CallStmt(Id("putFloat"),[BinaryOp('*',FloatLiteral(5.5),IntLiteral(2))])])])
    	expect = "9.0\n11.0"
    	self.assertTrue(TestCodeGen.test(input,expect,508))          

    def test_mulop_float9(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putFloat"),[BinaryOp('*',FloatLiteral(2.0),FloatLiteral(4.5))])])])
    	expect = "9.0"
    	self.assertTrue(TestCodeGen.test(input,expect,509))   

    def test_mulop_div_int10(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putFloatLn"),[BinaryOp('/',IntLiteral(1),IntLiteral(4))]),
                CallStmt(Id("putFloatLn"),[BinaryOp('/',FloatLiteral(2.0),FloatLiteral(4.5))]),
                CallStmt(Id("putFloatLn"),[BinaryOp('/',IntLiteral(2),FloatLiteral(5.0))]),
                CallStmt(Id("putFloat"),[BinaryOp('/',FloatLiteral(5.5),IntLiteral(2))])])])
    	expect = "0.25\n0.44444445\n0.4\n2.75"
    	self.assertTrue(TestCodeGen.test(input,expect,510))    

    def test_reop_int11(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBoolLn"),[BinaryOp('<',IntLiteral(1),IntLiteral(5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('<=',IntLiteral(1),IntLiteral(5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('>=',IntLiteral(1),IntLiteral(5))]),
                CallStmt(Id("putBool"),[BinaryOp('>',IntLiteral(1),IntLiteral(5))])])])
    	expect = "true\ntrue\nfalse\nfalse"
    	self.assertTrue(TestCodeGen.test(input,expect,511))   

    def test_reop_int_float12(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBoolLn"),[BinaryOp('<',IntLiteral(1),FloatLiteral(5.5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('<=',IntLiteral(1),FloatLiteral(5.5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('>=',IntLiteral(1),FloatLiteral(5.5))]),
                CallStmt(Id("putBool"),[BinaryOp('>',IntLiteral(1),FloatLiteral(5.5))])])])
    	expect = "true\ntrue\nfalse\nfalse"
    	self.assertTrue(TestCodeGen.test(input,expect,512))   

    def test_reop_int_float13(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBoolLn"),[BinaryOp('<',FloatLiteral(1.0),FloatLiteral(5.5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('<=',FloatLiteral(1.0),FloatLiteral(5.5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('>=',FloatLiteral(1.0),FloatLiteral(5.5))]),
                CallStmt(Id("putBool"),[BinaryOp('>',FloatLiteral(1.0),FloatLiteral(5.5))])])])
    	expect = "true\ntrue\nfalse\nfalse"
    	self.assertTrue(TestCodeGen.test(input,expect,513))   

    def test_reop_equal14(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBoolLn"),[BinaryOp('=',IntLiteral(1),IntLiteral(5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('<>',IntLiteral(1),IntLiteral(5))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('=',BooleanLiteral(True),BooleanLiteral(True))]),
                CallStmt(Id("putBool"),[BinaryOp('<>',BooleanLiteral(True),BooleanLiteral(True))])])])
    	expect = "false\ntrue\ntrue\nfalse"
    	self.assertTrue(TestCodeGen.test(input,expect,514)) 
 
    def test_div15(self):    
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putIntLn"),[BinaryOp('div',IntLiteral(4),IntLiteral(3))]),
                CallStmt(Id("putInt"),[BinaryOp('div',IntLiteral(6),IntLiteral(2))])])])
    	expect = "1\n3"
    	self.assertTrue(TestCodeGen.test(input,expect,515)) 

    def test_mod16(self):    
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putIntLn"),[BinaryOp('mod',IntLiteral(4),IntLiteral(3))]),
				CallStmt(Id("putInt"),[BinaryOp('mod',IntLiteral(6),IntLiteral(3))])])])
    	expect = "1\n0"
    	self.assertTrue(TestCodeGen.test(input,expect,516)) 

    def test_and17(self):    
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBoolLn"),[BinaryOp('and',BooleanLiteral(True),BooleanLiteral(True))]),
                CallStmt(Id("putBool"),[BinaryOp('and',BooleanLiteral(False),BooleanLiteral(True))])])])
    	expect = "true\nfalse"
    	self.assertTrue(TestCodeGen.test(input,expect,517)) 

    def test_or18(self):    
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBoolLn"),[BinaryOp('or',BooleanLiteral(True),BooleanLiteral(True))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('or',BooleanLiteral(False),BooleanLiteral(False))]),
				CallStmt(Id("putBool"),[BinaryOp('or',BooleanLiteral(False),BooleanLiteral(True))])])])
    	expect = "true\nfalse\ntrue"
    	self.assertTrue(TestCodeGen.test(input,expect,518)) 

    def test_reop_float_int19(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBoolLn"),[BinaryOp('<',FloatLiteral(21.5),IntLiteral(2))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('<=',FloatLiteral(21.5),IntLiteral(2))]),
                CallStmt(Id("putBoolLn"),[BinaryOp('>=',FloatLiteral(21.5),IntLiteral(2))]),
                CallStmt(Id("putBool"),[BinaryOp('>',FloatLiteral(21.5),IntLiteral(2))])])])
    	expect = "false\nfalse\ntrue\ntrue"
    	self.assertTrue(TestCodeGen.test(input,expect,519))   

    def test_var20(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("b"),IntType()),
                VarDecl(Id("c"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[IntLiteral(2)]),
                    CallStmt(Id("putInt"),[IntLiteral(2)])])])

        expect  = "2\n2"
        self.assertTrue(TestCodeGen.test(input,expect,520)) 

    def test_assign21(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("b"),IntType()),
                VarDecl(Id("c"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    Assign(Id('a'),IntLiteral(2)),
                    CallStmt(Id("putInt"),[Id('a')])])])

        expect  = "2\n2"
        self.assertTrue(TestCodeGen.test(input,expect,521)) 