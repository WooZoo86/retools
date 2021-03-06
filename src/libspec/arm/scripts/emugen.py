import os
import re
import json
import shutil
import logging
import tempfile
import argparse

from parser import ARMv7Parser
from specification import ARMv7OperationSpec, ARMv7Types, ARMv7Context
from ast.passes import IdentifierRenamer, ListAssignmentRewriter, SimpleFunctionOptimization
from ast.translators import InterpreterCPPTranslator, indent, NeedsSemiColon
from disgen import instruction_id_name

DEBUG = False

def method_name(ins_name):
    ins_name = re.sub('[\s\(\)\-\,\/\#]', '_', ins_name)
    ins_name = ins_name.replace("__", "_")
    ins_name = ins_name.rstrip("_")
    return "interpret_" + ins_name.lower()

def create_interpreter(interpreter_name_h, interpreter_name_cpp, symbols_file):
    """
    Create ARMInterpreter.h and ARMInterpreter.cpp.
    """
    # Inherit the basic types.
    known_types = list(ARMv7Types.known_types)

    # Load symbols file.
    symbols = None
    with open(symbols_file, "r") as fd:
        symbols = json.load(fd)

    with open(interpreter_name_h, "w") as fd:
        header = ""
        header += '#include "arm/ARMContext.h"\n'
        header += '#include "arm/ARMDisassembler.h"\n\n'
        header += '#include <memory>\n\n'
        header += 'using namespace Disassembler;\n\n'
        header += "class ARMInterpreter {\n"
        header += "public:\n"
        header += "    ARMInterpreter(ARMContext &ctx) :\n"
        header += "        m_ctx(ctx) {\n"
        header += "    }\n\n"
        header += "    void execute(const ARMInstruction &ins);\n\n"
        header += "private:\n"
        header += "    ARMContext &m_ctx;\n\n"
        header += "    bool ConditionPassed() { return true; }\n"
        header += "    bool CurrentModeIsHyp() { return false; }\n"
        header += "    bool CurrentModeIsNotUser() { return false; }\n"
        header += "    bool EventRegistered() { return false; }\n"
        header += "    bool HaveVirtExt() { return false; }\n"
        header += "    bool IsSecure() { return false; }\n"
        header += "    bool JazelleAcceptsExecution() { return false; }\n"
        header += "    void BKPTInstrDebugEvent() {}\n"
        header += "    void BranchWritePC(uint32_t address) {}\n"
        header += "    void CheckAdvSIMDEnabled() {}\n"
        header += "    void ClearEventRegister() {}\n"
        header += "    void EncodingSpecificOperations() {}\n"
        header += "    void Hint_Yield() {}\n"
        header += "    void SwitchToJazelleExecution() {}\n"
        header += "    void TakeHypTrapException() {}\n"
        header += "    void WaitForEvent() {}\n"
        header += "    void WaitForInterrupt() {}\n"
        header += "    ARMMode CurrentInstrSet() { return ARMMode_ARM; }\n"
        header += "    void SelectInstrSet(unsigned mode) {}\n"
        header += "    void BXWritePC(unsigned address) {}\n"
        header += "    void WriteHSR(unsigned ec, unsigned hsr_string) {}\n"
        header += "    unsigned ThisInstr() { return 0; }\n"
        header += "    bool Coproc_Accepted(unsigned cp_num, unsigned instr) { return true; }\n"
        header += "    void GenerateCoprocessorException() {}\n"
        header += "    void Coproc_InternalOperation(unsigned cp_num, unsigned instr) {}\n"
        header += "    unsigned ProcessorID() { return 0; }\n"
        header += "    void ClearExclusiveLocal(unsigned processorid) {}\n"
        header += "    unsigned CountLeadingZeroBits(unsigned value) {return 0;}\n"
        header += "    void CPSRWriteByInstr(unsigned value, unsigned byte_mask, bool is_exception_return) {}\n"
        header += "    void SPSRWriteByInstr(unsigned value, unsigned byte_mask) {}\n"
        header += "    void Hint_Debug(unsigned op) {}\n"
        header += "    void DataMemoryBarrier(unsigned domain, unsigned types) {}\n"
        header += "    void DataSynchronizationBarrier(unsigned domai, unsigned types) {}\n"
        header += "    bool CurrentModeIsUserOrSystem() { return true; }\n"
        header += "    bool HasVirtExt() { return true; }\n"
        header += "    void CallHypervisor(unsigned immediate) {}\n"
        header += "    void InstructionSynchronizationBarrier() {}\n"
        header += "    void NullCheckIfThumbEE(unsigned n) {}\n"
        header += "    void Coproc_SendLoadedWord(unsigned word, unsigned cp_num, unsigned instr) {}\n"
        header += "    bool Coproc_DoneLoading(unsigned cp_num, unsigned instr) { return true; }\n"
        header += "    void LoadWritePC(unsigned address) {}\n"
        header += "    bool UnalignedSupport() { return false; }\n"
        header += "    bool HaveLPAE() { return true; }\n"
        header += "    bool BigEndian() {return false;}\n"
        header += "    void SetExclusiveMonitors(unsigned address, unsigned size) {}\n"
        header += "    void Coproc_SendOneWord(unsigned word, unsigned cp_num, unsigned instr) {}\n"
        header += "    void Coproc_SendTwoWords(unsigned word2, unsigned word1, unsigned cp_num, unsigned instr) {}\n"
        header += "    unsigned SInt(unsigned value, unsigned bitsize) { return value; }\n"
        header += "    unsigned ArchVersion() { return 0; }\n"
        header += "    bool Coproc_DoneStoring(unsigned cp_num, unsigned instr) { return true; }\n"
        header += "    unsigned Coproc_GetOneWord(unsigned cp_num, unsigned instr) { return 0;}\n"
        header += "    std::tuple<unsigned, unsigned >Coproc_GetTwoWords(unsigned cp_num, unsigned instr) { return std::tuple<unsigned, unsigned>(0, 0); }\n"
        header += "    unsigned Coproc_GetWordToStore(unsigned cp_num, unsigned instr) { return 0; }\n"
        header += "    void BankedRegisterAccessValid(unsigned SYSm, unsigned mode) {}\n"
        header += "    void SPSRaccessValid(unsigned SYSm, unsigned mode) {}\n"
        header += "    void Hint_PreloadDataForWrite(unsigned address) {}\n"
        header += "    void Hint_PreloadData(unsigned address) {}\n"
        header += "    void Hint_PreloadInstr(unsigned address) {}\n"
        header += "    unsigned LowestSetBit(unsigned value) { return 0; }\n"
        header += "    unsigned PCStoreValue() { return 0; }\n"
        header += "    std::tuple<unsigned, bool> SignedSatQ(unsigned i, unsigned N) { return std::tuple<unsigned, unsigned>(0, false);}\n"
        header += "    std::tuple<unsigned, bool> UnsignedSatQ(unsigned i, unsigned N) { return std::tuple<unsigned, unsigned>(0, false); }\n"
        header += "    unsigned SignedSat(unsigned i, unsigned N) { return i; }\n"
        header += "    unsigned UnsignedSat(unsigned i, unsigned N) { return i; }\n"
        header += "    std::tuple<unsigned, bool> SatQ(unsigned i, unsigned N, bool unsigned_) { return std::tuple<unsigned, unsigned>(0, false); }\n"
        header += "    unsigned Sat(unsigned i, unsigned N, bool unsigned_) { return 0; }\n"
        header += "    bool IntegerZeroDivideTrappingEnabled() { return false; }\n"
        header += "    void GenerateIntegerZeroDivide() {}\n"
        header += "    unsigned RoundTowardsZero(unsigned val) { return val; }\n"
        header += "    void SendEvent() {}\n"
        header += "    bool HaveSecurityExt() { return true; }\n"
        header += "    void TakeSMCException() {}\n"
        header += "    bool ExclusiveMonitorsPass(unsigned address, unsigned size) { return false; }\n"
        header += "    void CallSupervisor(unsigned immediate) {}\n"
        header += "    unsigned Abs(unsigned value) { return value; }\n"
        header += "    bool CheckAdvSIMDOrVFPEnabled(bool include_fpexc_check, bool advsimd) { return true; }\n"
        header += "    unsigned FPAbs(unsigned operand) { return operand; }\n"
        header += "    void CheckVFPEnabled(bool value) { }\n"
        header += "    unsigned FPHalfToSingle(unsigned short operand, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned short FPSingleToHalf(unsigned operand, bool fpscr_controlled) { return 0; }\n"
        header += "    uint64_t FPSingleToDouble(uint32_t operand, bool fpscr_controlled) { return 0; }\n"
        header += "    uint32_t FPDoubleToSingle(uint64_t operand, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned FPMul(unsigned op1, unsigned op2, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned FPDiv(unsigned op1, unsigned op2, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned FPMulAdd(unsigned addend, unsigned op1, unsigned op2, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned FPNeg(unsigned operand) { return 0; }\n"
        header += "    void GenerateAlignmentException() {}\n"
        header += "    unsigned FixedToFP(unsigned operand, unsigned N, unsigned fraction_bits, bool unsigned_, bool round_to_nearest, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned FPToFixed(unsigned operand, unsigned M, unsigned fraction_bits, unsigned unsigned_, bool round_towards_zero, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned CountLeadingSignBits(unsigned val) { return 0; }\n"
        header += "    unsigned FPZero(unsigned sign, unsigned N) { return 0; }\n"
        header += "    unsigned FPTwo(unsigned N) { return 0; }\n"
        header += "    unsigned FPThree(unsigned N) { return 0; }\n"
        header += "    unsigned FPMaxNormal(unsigned sign, unsigned N) { return 0; }\n"
        header += "    unsigned FPInfinity(unsigned sign, unsigned N) { return 0; }\n"
        header += "    unsigned FPDefaultNaN(unsigned N) { return 0; }\n"
        header += "    unsigned FPAdd(unsigned op1, unsigned op2, bool fpscr_controlled) { return 0; }\n"
        header += "    unsigned FPSub(unsigned op1, unsigned op2, bool fpscr_controlled) { return 0; }\n"
        header += "    bool FPCompareGT(unsigned op1, unsigned op2, bool fpscr_controlled) { return false; }\n"
        header += "    void SerializeVFP() {}\n"
        header += "    void VFPExcBarrier() {}\n"
        header += "    unsigned Ones(unsigned n) { return 0; }\n"
        header += "    void NullCheckIfThumbEE() {}\n"
        header += "    unsigned FPSqrt(unsigned operand) { return 0; }\n"
        header += "    unsigned FPRSqrtStep(unsigned op1, unsigned op2) { return 0; }\n"
        header += "    unsigned UnsignedRSqrtEstimate(unsigned operand) { return 0; }\n"
        header += "    unsigned FPRSqrtEstimate(unsigned operand) { return 0; }\n"
        header += "    unsigned FPRecipStep(unsigned op1, unsigned op2) { return 0; }\n"
        header += "    unsigned UnsignedRecipEstimate(unsigned operand) { return 0; }\n"
        header += "    unsigned FPRecipEstimate(unsigned operand) { return 0; }\n"
        header += "    bool FPCompareGE(unsigned op1, unsigned op2, bool fpscr_controlled) { return false; }\n"
        header += "    std::tuple<bool, bool, bool, bool> FPCompare(unsigned op1, unsigned op2, bool quiet_nan_exc, bool fpscr_controlled) { return std::tuple<bool, bool, bool, bool>(false, false, false, false); }\n"
        header += "    bool FPCompareEQ(unsigned op1, unsigned op2, bool fpscr_controlled) { return false; }\n"
        header += "    template<class T> const T& Max(const T& a, const T& b) { return (a < b) ? b : a; }\n"
        header += "    template<class T> const T& Min(const T& a, const T& b) { return (a < b) ? a : b; }\n"
        header += "    template<class T> const T& FPMax(const T& a, const T& b, bool val) { return (a < b) ? b : a; }\n"
        header += "    template<class T> const T& FPMin(const T& a, const T& b, bool val) { return (a < b) ? a : b; }\n"
        header += "    unsigned PolynomialMult(unsigned op1, unsigned op2) { return 0; }\n"
        header += "\n"

        fd.write(header)
        for instruction in ARMv7OperationSpec.instructions:
            ins_name = instruction["name"]
            fd.write("    bool %s(const ARMInstruction &ins);\n" % method_name(ins_name))

        fd.write("};\n")

    with open(interpreter_name_cpp, "w") as fd:
        header = ""
        header += '#include "arm/gen/ARMInterpreter.h"\n'
        header += '#include "arm/gen/ARMDecodingTable.h"\n'
        header += '#include "arm/ARMContext.h"\n'
        header += '#include "arm/ARMUtilities.h"\n'
        header += '#include "Utilities.h"\n\n'
        header += '#include <tuple>\n'
        header += '#include <memory>\n\n'
        header += 'using namespace std;\n\n'

        fd.write(header)

        # Create the execution dispatcher.
        body = ""
        body += "void ARMInterpreter::execute(const ARMInstruction &ins) {\n"
        body += "    switch (ins.id) {\n"
        for i, instruction in enumerate(ARMv7OperationSpec.instructions):
            body += "        case ARMInstructionId::%s: %s(ins); break;\n" % (instruction_id_name(instruction), method_name(instruction["name"]))
        body += "        default: break;\n"
        body += "    }\n"
        body += "}\n\n"
        fd.write(body)

        # Fix the type name of variables that are in ARMContext by adding the 'm_ctx.' prefix.
        for entry in known_types:
            original_name = entry["name"]
            real_name = original_name.split(".", 1)[0]
            if real_name in ARMv7Context.field_names:
                entry["name"] = "m_ctx." + original_name

        for i, instruction in enumerate(ARMv7OperationSpec.instructions):
            ins_name = instruction["name"]
            logging.info("Processing instruction '%s' (%d)" % (ins_name, i))

            fd.write("bool ARMInterpreter::%s(const ARMInstruction &ins) {\n" % method_name(ins_name))

            ins_operation = instruction["operation"]

            # Remove empty lines, because I suck at parsing.
            ins_operation = os.linesep.join([s for s in ins_operation.splitlines() if not re.match(r'^\s*$', s)])

            # Get the AST for the decoder pseudocode and translate it to C++.
            program_ast = ARMv7Parser.parse_program(ins_operation)

            # Expand the known_types with the instruction fields.
            ins_types = list(known_types)
            ins_id = instruction_id_name(instruction)
            for symbol in symbols[ins_id]:
                symbol = "ins." + symbol
                ins_types.append({"name" : symbol, "type" : ("int", 32)})

            # Remove useless elements from AST.
            SimpleFunctionOptimization().transform(program_ast)

            # Convert all the local variables to instance variables.
            IdentifierRenamer(symbols[ins_id], "ins.").transform(program_ast)

            # Add the m_ctx prefix to variables present in ARMContext.
            IdentifierRenamer(ARMv7Context.field_names, "m_ctx.").transform(program_ast)

            # Fix untranslatable list assignments.
            ListAssignmentRewriter().transform(program_ast)

            # Create a translator.
            translator = InterpreterCPPTranslator(known_types=ins_types)

            body = ""

            # For each of the statements, do a translation.
            for ast_statement in program_ast:
                code = translator.accept(None, ast_statement)
                if NeedsSemiColon(ast_statement):
                    code += ";"

                body += indent(code)

            # TODO: Do the proper thing.
            for var in translator.define_me:
                type_ = "int"
                if var == "imm64":
                    type_ = "uint64_t"

                fd.write("    %s %s = 0;\n" % (type_, var))

            if len(translator.define_me):
                fd.write("\n")

            # Write the translated body.
            fd.write(body)
            fd.write("    return true;\n")
            fd.write("}\n")
            fd.write("\n")

    return True

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Generator.')
    parser.add_argument("-o", "--directory", default="../gen/", help="Directory where the generated files will be placed.")
    parser.add_argument("-g", "--generate", action='store_true', help="Generate ARMInterpreter[.h|.cpp]")
    parser.add_argument("-d", "--debug", action='store_true', help="Enable debugging information, just for developers.")
    parser.add_argument("-n", "--dry_mode", action='store_true', help="Do not write output to files.")

    args = parser.parse_args()

    DRY_MODE = args.dry_mode
    DEBUG = args.debug
    gen_decoder = args.generate

    if not gen_decoder:
        logging.error("Nothing to generate, please choose one option")
        parser.print_help()
        return False

    # Create dummy 'gen' dir and dummy 'symbols.sym'.
    if DRY_MODE:
        logging.info("Running in dry mode, I will not actually write any output.")
        args.directory = tempfile.mkdtemp()
        open(os.path.join(args.directory, "symbols.sym"), "a").close()

    # Filenames and path's.
    gen_dir = os.path.abspath(args.directory)
    symbols_file = os.path.join(gen_dir, "symbols.sym")
    interpreter_name_h = os.path.join(gen_dir, "ARMInterpreter.h")
    interpreter_name_cpp = os.path.join(gen_dir, "ARMInterpreter.cpp")

    if not os.path.exists(gen_dir):
        logging.info("Directory '%s' does not exist, creating it ..." % gen_dir)
        os.makedirs(gen_dir)

    if not os.path.exists(symbols_file):
        logging.error("Symbol file '%s' does not exist, error ..." % symbols_file)
        return False

    if os.path.exists(interpreter_name_h):
        logging.info("Removing file '%s' ..." % interpreter_name_h)
        os.remove(interpreter_name_h)

    if os.path.exists(interpreter_name_cpp):
        logging.info("Removing file '%s' ..." % interpreter_name_cpp)
        os.remove(interpreter_name_cpp)

    logging.info("Placing all the generated files in '%s'." % gen_dir)
    logging.info("Creating interpreter at '%s'." % interpreter_name_h)
    logging.info("Creating interpreter at '%s'." % interpreter_name_cpp)
    logging.info("Loading symbol table from '%s'." % symbols_file)

    if not create_interpreter(interpreter_name_h, interpreter_name_cpp, symbols_file):
        logging.error("Could not create the interpreter.")
        return False

    logging.info("Finished creating autogenerated stubs.")
    return True

if __name__ == '__main__':
    main()
