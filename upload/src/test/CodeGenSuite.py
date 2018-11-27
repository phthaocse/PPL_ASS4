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

    # def test_reop_int_float12(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],[],[
    # 			CallStmt(Id("putFloatLn"),[BinaryOp('<',IntLiteral(1),FloatLiteral(5.5))]),
    #             CallStmt(Id("putFloatLn"),[BinaryOp('<=',IntLiteral(1),FloatLiteral(5.5))]),
    #             CallStmt(Id("putFloatLn"),[BinaryOp('>=',IntLiteral(1),FloatLiteral(5.5))]),
    #             CallStmt(Id("putFloat"),[BinaryOp('>',IntLiteral(1),FloatLiteral(5.5))])])])
    # 	expect = "true\ntrue\nfalse\nfalse"
    # 	self.assertTrue(TestCodeGen.test(input,expect,512))   

 

    
