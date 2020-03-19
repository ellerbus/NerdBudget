from django.test import TestCase

from .models import Ledger


class LedgerTestCase(TestCase):
    def setUp(self):
        pass

    def test_parse_as_withdrawal(self):
        date = '02/09/2015'
        descr = 'NN NNNN 0010 NNN# 9999999 99999 NNNNNNN NNNN'
        pattern = 'NNNNNN0010NNN#{NBR}NNNNNNNNNNN'
        amount = '$1,400.00'
        balance = '$1,138.52'
        text = f'{date}\t{descr}\tREF\t{amount}\t\t{balance}\tNNNNNNNNNNN NNNNNNN'
        ledger = Ledger(original_text=text)
        ledger.parse()
        self.assertEqual(ledger.date, '2015-02-09')
        self.assertEqual(ledger.description, descr)
        self.assertEqual(ledger.pattern, pattern)
        self.assertEqual(ledger.amount, -1400)
        self.assertEqual(ledger.balance, 1138.52)
        # Assert.AreEqual(@'NNNNNNN0010NNN#[0-9]+NNNNNNNNNNN', ledger.RegexMap);

    def test_parse_as_deposit(self):
        date = '02/09/2015'
        descr = 'NN NNNN 0010 NNN# 9999999 99999 NNNNNNN NNNN'
        pattern = 'NNNNNN0010NNN#{NBR}NNNNNNNNNNN'
        amount = '$1,400.00'
        balance = '$1,138.52'
        text = f'{date}\t{descr}\tREF\t\t{amount}\t{balance}\tNNNNNNNNNNN NNNNNNN'
        ledger = Ledger(original_text=text)
        ledger.parse()
        self.assertEqual(ledger.date, '2015-02-09')
        self.assertEqual(ledger.description, descr)
        self.assertEqual(ledger.pattern, pattern)
        self.assertEqual(ledger.amount, 1400)
        self.assertEqual(ledger.balance, 1138.52)
        # Assert.AreEqual(@'NNNNNNN0010NNN#[0-9]+NNNNNNNNNNN', ledger.RegexMap);

    def test_parse_actual(self):
        text = '02/29/2020\tCONF # 12 REF # 34 SQ *ROOTS RAW JUICE LAKE MARY FL 02/29/20\t0000709613\t$ 10.16\t\t$ 828.92\tInquire'
        ledger = Ledger(original_text=text)
        ledger.parse()
        self.assertEqual(ledger.date, '2020-02-29')
        self.assertEqual(ledger.description,
                         'CONF # 12 REF # 34 SQ *ROOTS RAW JUICE LAKE MARY FL 02/29/20')
        self.assertEqual(ledger.pattern,
                         '{CONF}{REF}SQROOTSRAWJUICELAKEMARYFL{DATE}')
        self.assertEqual(ledger.amount, -10.16)
        self.assertEqual(ledger.balance, 828.92)

#         [TestMethod]
#         public void Ledger_Should_Parse_001()
#         {
#             var ledger = new Ledger
#             {
#                 OriginalText = '02/09/2015	NNNNNNNN'N N99999 NNNNNNN NN 02/08/15 NNN 9999	REF 	$9.82		$2,538.52	NNNNNNNNNNN NNNNNNN'
#             };

#             Assert.AreEqual('10D9DAF6', ledger.Id);
#             Assert.AreEqual(new DateTime(2015, 2, 9), ledger.Date);
#             Assert.AreEqual('NNNNNNNN'N N99999 NNNNNNN NN 02/08/15 NNN 9999', ledger.Description);
#             Assert.AreEqual(-9.82, ledger.Amount);
#             Assert.AreEqual(2538.52, ledger.Balance);
#             Assert.AreEqual(@'NNNNNNNNNN99999NNNNNNNNN\(MDY\)NNN9999', ledger.RegexMap);
#         }

#         [TestMethod]
#         public void Ledger_Should_Parse_002()
#         {
#             var ledger = new Ledger
#             {
#                 OriginalText = '02/09/2015	NNNNNNNN : NNNNNNNN NN: 99999999NN: NNNNNNNN NNN NNNNN 99999999		REF 	$1,406.00	$2,548.34	NNNNNNNNNNN NNNNNNN'
#             };

#             Assert.AreEqual('999BEDC8', ledger.Id);
#             Assert.AreEqual(new DateTime(2015, 2, 9), ledger.Date);
#             Assert.AreEqual('NNNNNNNN : NNNNNNNN NN: 99999999NN: NNNNNNNN NNN NNNNN 99999999', ledger.Description);
#             Assert.AreEqual(1406, ledger.Amount);
#             Assert.AreEqual(2548.34, ledger.Balance);
#             Assert.AreEqual(@'NNNNNNNNNNNNNNNNNN99999999NNNNNNNNNNNNNNNNNN99999999', ledger.RegexMap);
#         }

#         [TestMethod]
#         public void Ledger_Should_Parse_003()
#         {
#             var ledger = new Ledger
#             {
#                 OriginalText = '02/09/2015	NNNNNNN NNNNNNNN #9999 NNNNNNN NN 02/08/15 NNN 9999	$17.81		REF 	$1,142.34	NNNNNNNNNNN NNNNNNN'
#             };

#             Assert.AreEqual('98AEE42E', ledger.Id);
#             Assert.AreEqual(new DateTime(2015, 2, 9), ledger.Date);
#             Assert.AreEqual('NNNNNNN NNNNNNNN #9999 NNNNNNN NN 02/08/15 NNN 9999', ledger.Description);
#             Assert.AreEqual(-17.81, ledger.Amount);
#             Assert.AreEqual(1142.34, ledger.Balance);
#             Assert.AreEqual(@'NNNNNNNNNNNNNNN#[0-9]+NNNNNNNNN\(MDY\)NNN9999', ledger.RegexMap);
#         }

#         [TestMethod]
#         public void Ledger_Should_Parse_004()
#         {
#             var ledger = new Ledger
#             {
#                 OriginalText = '02/07/2015	9999-NNNN NNN NNN N-9999, 9999 NN NNNNNNN NN NNN 9999	$68.16		REF 	$1,218.82	NNNNNNNNNNN NNNNNNN'
#             };

#             Assert.AreEqual('X6A9645D', ledger.Id);
#             Assert.AreEqual(new DateTime(2015, 2, 7), ledger.Date);
#             Assert.AreEqual('9999-NNNN NNN NNN N-9999, 9999 NN NNNNNNN NN NNN 9999', ledger.Description);
#             Assert.AreEqual(-68.16, ledger.Amount);
#             Assert.AreEqual(1218.82, ledger.Balance);
#             Assert.AreEqual(@'9999NNNNNNNNNNN99999999NNNNNNNNNNNNNN9999', ledger.RegexMap);
#         }

#         #endregion

#         #region Collection Tests

#         [TestMethod]
#         public void LedgerCollection_Should_FindMissingBudget()
#         {
#             //  assign
#             var account = Builder<Account>.CreateNew().Build();

#             var ledger = CreateEmptyLedger();

#             //  act
#             account.Ledgers.Add(ledger);

#             //  assert
#             Assert.AreEqual(1, account.Ledgers.MissingBudget().Count());
#         }

#         [TestMethod]
#         public void LedgerCollection_Should_FindLedger()
#         {
#             //  assign
#             var account = Builder<Account>.CreateNew().Build();

#             var ledger = CreateEmptyLedger();

#             //  act
#             account.Ledgers.Add(ledger);

#             //  assert
#             var x = account.Ledgers.Find(ledger.Id.ToLower(), ledger.Date);

#             Assert.AreSame(ledger, x);
#         }

#         [TestMethod]
#         public void LedgerCollection_Should_FindMap()
#         {
#             //  assign
#             var account = CreateAccount();

#             var ledger = CreateEmptyLedger();

#             var map = new Map { RegexPattern = ledger.RegexMap, BudgetId = account.Categories.First().Budgets.First().Id };

#             account.Maps.Add(map);

#             //  act
#             account.Ledgers.Import(ledger.OriginalText);

#             //  assert
#             Assert.AreEqual(map.BudgetId, account.Ledgers.First().BudgetId);
#         }

#         private Account CreateAccount()
#         {
#             var account = Builder<Account>.CreateNew().Build();

#             var category = Builder<Category>.CreateNew().Build();

#             var budget = new Budget { CategoryId = category.Id, Id = 'X' };

#             var po = new PrivateObject(account);

#             po.SetField('_categories', null);
#             po.SetProperty('AllCategories', new List<Category> { category });

#             po.SetField('_budgets', null);
#             po.SetProperty('AllBudgets', new List<Budget> { budget });

#             return account;
#         }

#         [TestMethod]
#         public void LedgerCollection_Should_AssignAccountId()
#         {
#             //  assign
#             var account = Builder<Account>.CreateNew().Build();

#             var ledger = CreateEmptyLedger();

#             //  act
#             account.Ledgers.Add(ledger);

#             //  assert
#             Assert.AreEqual(account.Id, ledger.AccountId);
#         }

#         [TestMethod]
#         public void LedgerCollection_Should_LookupUsingId()
#         {
#             //  assign
#             var account = Builder<Account>.CreateNew().Build();

#             var l1 = CreateEmptyLedger();

#             //  act
#             account.Ledgers.Add(l1);

#             //  assert
#             Assert.AreEqual(l1, account.Ledgers.First());
#         }

#         [TestMethod]
#         public void LedgerCollection_Should_ParseInputAndUpdateBalances()
#         {
#             //  assign
#             var account = Builder<Account>.CreateNew().Build();

#             var input = @'02/09/2015	NN NNNNN 0010 NNN# 9999999 99999 NNNNNNN NNNN	$1,400.00		$1,138.52	NNNNNNNNNNN NNNNNNN
# 02/09/2015	NNNNNNNN'N N99999 NNNNNNN NN 02/08/15 NNN 9999	$9.82		$2,538.52	NNNNNNNNNNN NNNNNNN
# 02/09/2015	NNNNNNNN : NNNNNNNN NN: 99999999NN: NNNNNNNN NNN NNNNN 99999999		$1,406.00	$2,548.34	NNNNNNNNNNN NNNNNNN
# 02/09/2015	NNNNNNN NNNNNNNN #2189 NNNNNNN NN 02/08/15 NNN 5231	$17.81		$1,142.34	NNNNNNNNNNN NNNNNNN
# 02/08/2015	NNNNNNNN'N N99999 NNNNNNN NN 02/07/15 NNN 9999	$13.80		$1,160.15	NNNNNNNNNNN NNNNNNN
# 02/08/2015	NNNN'N NNN NNNN #3 NNNNNNN NN 02/07/15 NNN 7542	$10.00		$1,173.95	NNNNNNNNNNN NNNNNNN
# 02/08/2015	NNNNNN 10250 NNNNN NNNN N NNNNNNN NN NNN 5411	$17.47		$1,183.95	NNNNNNNNNNN NNNNNNN
# 02/07/2015	NNNNNN 10250 NNNNN NNNN N NNNNNNN NN NNN 5411	$17.40		$1,201.42	NNNNNNNNNNN NNNNNNN
# 02/07/2015	10726-NNNN NNN NNN N-260, 4200 NN NNNNNNN NN NNN 5691	$68.16		$1,218.82	NNNNNNNNNNN NNNNNNN
# 02/07/2015	NNN - N-NNNN N/N 407-690-5000 NN 02/07/15 NNN 4784	$55.00		$1,286.98	NNNNNNNNNNN NNNNNNN';

#             //  act
#             account.Ledgers.Import(input);

#             //  assert
#             Assert.AreEqual(10, account.Ledgers.Count);

#             Assert.AreEqual(2, account.Balances.Count);

#             Assert.IsTrue(account.Balances.Contains(new DateTime(2015, 2, 1)));

#             Assert.IsTrue(account.Balances.Contains(new DateTime(2015, 2, 6)));
#         }

#         [TestMethod]
#         public void LedgerCollection_Should_ParseEmptyInput()
#         {
#             //  assign
#             var account = Builder<Account>.CreateNew().Build();

#             var input = @'';

#             //  act
#             account.Ledgers.Import(input);

#             //  assert
#             Assert.AreEqual(0, account.Ledgers.Count);
#         }

#         [TestMethod]
#         public void LedgerCollection_Should_ParseDuplicateInput()
#         {
#             //  assign
#             var account = Builder<Account>.CreateNew().Build();

#             var input = @'02/09/2015	NN NNNNN 0010 NNN# 9999999 99999 NNNNNNN NNNN	$1,400.00		$1,138.52	NNNNNNNNNNN NNNNNNN
# 02/09/2015	NN NNNNN 0010 NNN# 9999999 99999 NNNNNNN NNNN	$1,400.00		$1,138.52	NNNNNNNNNNN NNNNNNN';

#             //  act
#             account.Ledgers.Import(input);

#             //  assert
#             Assert.AreEqual(1, account.Ledgers.Count);
#         }

#         #endregion
#     }
# }
