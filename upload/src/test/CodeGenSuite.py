import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):

    def test_int_ast(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putInt"),[IntLiteral(5)])])])
    	expect = "5"
    	self.assertTrue(TestCodeGen.test(input,expect,500))


    def test_float_ast(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putFloatLn"),[FloatLiteral(5.5)])])])
    	expect = "5.5\n"
    	self.assertTrue(TestCodeGen.test(input,expect,501))

    def test_bool_ast(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putBool"),[BooleanLiteral(False)])])])
    	expect = "false"
    	self.assertTrue(TestCodeGen.test(input,expect,502))

    def test_string_ast(self):
    	input = Program([
    		FuncDecl(Id("main"),[],[],[
    			CallStmt(Id("putString"),[StringLiteral("Thao")])])])
    	expect = "Thao"
    	self.assertTrue(TestCodeGen.test(input,expect,503))
