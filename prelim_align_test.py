import unittest
from align_ngs_codons import prelim_align
from align_ngs_codons import gap_padding
from align_ngs_codons import translate_dna


class MyTestCase(unittest.TestCase):

    #Todo add more tests to prelim aign (indels start offset...)
    # @unittest.skip('Skip this test')
    def test_prelim_align(self):
        reference = "ATGACAGTGATGGGGATACAGAAGAATTACCAACAGTGGTGGATATGGGGAATCTTAGGCTTTTGGATGCTAATGATTTGTAATGGGAATGACACGTGGGTCACAGTATATTATGGGGTACCTGTGTGGAGAGAAGCAAAAACTACTCTATTCTGTGCATCAGATGCTAAAGCATATGAGAAAGAAGTGCATAATGTTTGGGCTACACATGCCTGTGTACCCACAGACCCCAACCCACAAGAAATGGTTTTGGAAAATGTAACAGAAAATTTTAACATGTGGAAAAATGACATGGTAGATCAGATGCATGAAGATATAATCAGTTTATGGGATCAAAGCCTCAAGCCATGTGTAAAGTTGACCCCGCTCTGTGTCACTTTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTTTGACCCAATTCCTATACATTATTGTGCTCCAGCTGGTTTTGCGATTCTAAAGTGTAATAATAAGACATTCAATGGCACAGGACCATGCAATAATGTCAGCACAGTACAATGTACACATGGGATTAGGCCAGTGGTCTCAACTCAACTATTGTTAAATGGTAGCCTAGCAGAAAAAGAGATAATAATTAGATCTGAAAATCTGACAAACAATATCAAAACAATAATAGTACATCTCAATGAATCTGTAGAGATTAATTGTATAAGACCCAATAATAATACAAGGAAAAGTATGAGAATAGGACCAGGACAAACATTCTATGCAACAGGAGAAATAATAGGAGATATAAGGCAAGCACATTGTAACATTAGCAAAGATAAATGGGACAAAACTTTACACAGGGTAAGTGAAAAATTAAGAGAACACTTCCCTAATAAGACAATAACATTTAACTCATCCTCAGGAGGAGACCTAGAAATTACAACACATAGCTTTAATTGTGGAGGAGAATTTTTCTATTGCAATACATCAGGCCTGTTTAATAGTACATTTAATACTACATTTTATGAACCTTCAAATTTAACCATCACACTCCAATGCAGAATAAAACAAATTATAAACATGTGGCAGGAGGTGGGACGAGCAATGTATGCCCCTCCCATTGCAGGAAACATAACATGTGAATCAAAGATCACAGGGCTAATATTGACACGTGATGGAGGAAGTGACAATGGGACAGAGACATTCAGACCTGGAGGAGGAGATATGAGGGACAACTGGAGAAGTGAATTATATAAATATAAAGTGGTAGAAATTAAGCCATTGGGAATAGCACCCACTAATGGAAGAAGGAGAGTGGTGCAGAGAGAGAAAAGAGCAGTGGGAATAGGAGCTGTATTCCTTGGGTTCTTGGGAGCAGCAGGAAGCACTATGGGCGCGGCATCAATAACGCTGACGGTACAGGCCAGACAATTATTGTCTGGTATAGTGCAACAGCAAAACAATTTGCTGAGGGCTATAGAGGCGCAACAGCATATGTTGCAACTCACGGTCTGGGGCATTAAGCAGCTCCAGGCAAGAGTCTTGGCTCTAGAAAGATACCTAAGGGATCAACAGCTCCTAGGGATGTGGGGCTGCTCTGGAAAACTCATCTGCACCACTAATGTGGCTTGGAACTCTAGTTGGAGTAATAAAAGTCAAGATGAGATTTGGAAGAACATGACCTGGATGCAGTGGGATAGAGAAATTAGTGACTATACAAACACAATATACAGGTTGCTTGAAGAGTCGCAAAACCAGCAAGAAATAAATGAAAAAGATTTACTAGCATTGGACAGTTGGAACAATCTGTGGACTTGGTTTGACATAACAAACTGGCTGTGGTATATAAAAATATTCATAATGATAGTAGGAGGCTTGATAGGGTTAAGAATAATTTTTGCTGTGCTTTCTCTAGTGAATAGAGTTAGGCAGGGATACTCACCTTTGTCGTTGCAGACCTTTACCCCAAACCCGAGGGGACCCGACAGGCTCGAAAGAATCGAAGAAGAAGGTGGAGAGCAAGACAGAGACAGATCCGTGCGATTAGTGAGCGGATTCTTAGCACTTGCCTGGGACGACCTGCGGAGCCTGTGCCTCTTCAGCTATCACCTATTGAGAGACTTCATATTGGTTGCAGCGAGAGCAGTGGGACTTCTGGGACGCAGCAGTCTCAGGGGACTACAGACAGGGTGGGAAGCCCTTAAGTATCTGGGAAGCCTTGTGCAATATTGGGGTCTAGAGCTAAAAAAGAGTGCTATTAGTCTGCTTGATACCTTAGCAATAGCAGTAGCTGAAGGAACAGATAGGATTATAGAATTCATACAAAGAATTTGTAGAGCTATCCTCCATATACCTAGAAGAATAAGACAGGGCTTTGAAGCAGCTTTGCTA"
        test_in = {"CAP255_2000_C1C3_good_start_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_good_start_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        for name, seq in test_in.items():
            seq_align, ref_align, frame = prelim_align(test_in[name], reference, name)
            self.assertEquals(seq_align, test_out[name])


    # @unittest.skip('Skip this test')
    def test_start_1_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_good_start_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        ref_in = {"ref_start_1": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAA---TAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_good_start_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_start_1"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_start_2_gap_padding(self):
        frame = 2
        test_in = {"CAP255_2000_C1C3_good_start_2": "TTTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        ref_in = {"ref_start_2": "TTTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAA---TAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_good_start_2": "--TTTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_start_2"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_start_3_gap_padding(self):
        frame = 1
        test_in = {"CAP255_2000_C1C3_good_start_3": "CTTTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        ref_in = {"ref_start_3": "CTTTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAA---TAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_good_start_3": "-CTTTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_start_3"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_1_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATT-GAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        ref_in = {"ref_del_1": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATT-GAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_del_1"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_2_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCA-AATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        ref_in = {"ref_del_2": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCA-AATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_del_2"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_3_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAATTG-ACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTTT"}
        ref_in = {"ref_del_3": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTTT"}
        test_out = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAATTG-ACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTTT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_del_3"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_2_or_3_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAA-TGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        ref_in = {"ref_del_2_or_3": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAA-TGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_del_2_or_3"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_ins_1_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_ins_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        ref_in = {"ref_ins_1": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAA---TAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGG-AAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_ins_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAA--AAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_ins_1"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_ins_2_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_ins_2": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        ref_in = {"ref_ins_2": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAA---TAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAA-GGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_ins_2": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGG--GAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_ins_2"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_ins_3_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_ins_3": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        ref_in = {"ref_ins_3": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAA---TAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTC-TTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_ins_3": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCT--TTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_ins_3"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_large_gap_padding(self):
        frame = 0
        test_in = {"CAP255_2000_C1C3_good_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAATTGCACTTTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        ref_in = {"ref_large_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAACTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_good_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAATTGCACTTTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        for name, seq in test_in.items():
            padded_sequence = gap_padding(seq, ref_in["ref_large_del"], frame, seq.replace("-", ""), name)
            self.assertEquals(padded_sequence, test_out[name])


    # @unittest.skip('Skip this test')
    def test_start_1_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_good_start_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_good_start_1": "LNCSNASSNANVTKVDNSSTIGEIKNCTFNVTTELRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_start_2_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_good_start_2": "--TTTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_good_start_2": "XLNCSNASSNANVTKVDNSSTIGEIKNCTFNVTTELRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_start_3_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_good_start_3": "-CTTTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_good_start_3": "XLNCSNASSNANVTKVDNSSTIGEIKNCTFNVTTELRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_1_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATT-GAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_del": "LNCSNANSNTNVTDIDNSTIXEIKNCTFNVTTELRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVSX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_2_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCA-AATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_del": "LNCSNANSNTNVTDIDNSXIGEIKNCTFNVTTELRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVSX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_3_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAATTG-ACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTTT"}
        test_out = {"CAP255_2000_C1C3_del": "LNCSNANSNTNVTDIDNSTIGEIKNXTFNVTTELRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVSF"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_2_or_3_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAA-TGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_del": "LNCSNANSNTNVTDIDNSTXGEIKNCTFNVTTELRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVSX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_ins_1_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_ins_1": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAA--AAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_ins_1": "LNCSNASSNANVTKVDNSSTIGEIKNCTFNVTTELRDKEXKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_ins_2_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_ins_2": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGG--GAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_ins_2": "LNCSNASSNANVTKVDNSSTIGEIKNCTFNVTTELRDKXEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_ins_3_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_ins_3": "TTAAACTGTAGCAATGCAAGTAGCAATGCAAATGTCACAAAGGTTGATAATAGTAGCACAATTGGAGAAATAAAGAATTGCACTTTCAATGTAACTACAGAATTAAGAGATAAGGAAAAGAAAGAAAATGCACTCT--TTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTTAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCT"}
        test_out = {"CAP255_2000_C1C3_ins_3": "LNCSNASSNANVTKVDNSSTIGEIKNCTFNVTTELRDKEKKENALXFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


    # @unittest.skip('Skip this test')
    def test_del_large_translate_dna(self):
        test_in = {"CAP255_2000_C1C3_good_del": "TTAAACTGTAGCAATGCAAATAGCAATACAAATGTCACAGATATTGATAATAGCACAATTGGAGAAATAAAGAATTGCACTTTAAGAGATAAGGAAAAGAAAGAAAATGCACTCTTTTATAAACTTGATATAGTACCACTTAATGGAAATAACAACAGCAGCTTCAGTATGTATAGATTAATAAACTGTAATACCTCAGTCGTAACACAAGCCTGTCCAAAGGTCTCTTT"}
        test_out = {"CAP255_2000_C1C3_good_del": "LNCSNANSNTNVTDIDNSTIGEIKNCTLRDKEKKENALFYKLDIVPLNGNNNSSFSMYRLINCNTSVVTQACPKVSX"}
        for name, seq in test_in.items():
            prot_seq = translate_dna(seq)
            self.assertEquals(prot_seq, test_out[name])


if __name__ == '__main__':
    unittest.main()
