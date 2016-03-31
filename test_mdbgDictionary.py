
import unittest
import mdbgCedict 

class TestMdbgDictionary(unittest.TestCase):

  def setUp(self):
      self.mdbgdict = mdbgCedict.MdbgCedict()

  def test_lookup_nihao(self):
      entries = [entry for entry in self.mdbgdict.get_entries_for_simplified('你好')]
      self.assertTrue(len(entries) > 0)
      self.assertIn('hi!', [english.lower() for english in entries[0].englishdefinitions])

  def test_lookup_zhuyi(self):
      entries = [entry for entry in self.mdbgdict.get_entries_for_simplified('注意')]
      self.assertTrue(len(entries) > 0)
      self.assertEqual('zhu4yi4', entries[0].pinyin.lower())
      self.assertEqual('zhuyi', entries[0].pinyin_no_tones)
      

      
if __name__ == '__main__':
    unittest.main()
