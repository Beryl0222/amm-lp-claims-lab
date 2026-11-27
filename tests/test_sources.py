"""检查离线资料的格式、引用和业务时点。"""
from pathlib import Path
import unittest

from inspect_inputs import read_table


DATA = Path(__file__).resolve().parents[1] / "data"
FIELDS = {
    'pool_policy': ['pool', 'token0', 'token1', 'protocol_bps', 'opening_tick'],
    'initial_positions': ['position', 'pool', 'owner', 'lower', 'upper', 'liquidity'],
    'position_ops': ['op', 'order', 'known', 'position', 'kind', 'holder', 'units'],
    'route_legs': ['id', 'route', 'order', 'known', 'pool', 'from_tick', 'to_tick', 'asset', 'fee', 'revises'],
    'route_receipts': ['receipt', 'route', 'seen', 'status', 'legs', 'fees', 'revises'],
    'fee_treasury': ['fact', 'step', 'pool', 'asset', 'kind', 'owner', 'payment', 'amount'],
}


class InputBundleTest(unittest.TestCase):
    def test_csv_contract(self):
        self.assertEqual({p.stem for p in DATA.glob("*.csv")}, set(FIELDS))
        for name, expected in FIELDS.items():
            with self.subTest(table=name):
                fields, rows = read_table(DATA, name)
                self.assertEqual(fields, expected)
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_records(self):
        _, records = read_table(DATA, 'route_legs')
        legs = {row['id']: row for row in records}
        _, records = read_table(DATA, 'position_ops')
        ops = {row['op']: row for row in records}
        _, records = read_table(DATA, 'route_receipts')
        routes = {row['receipt']: row for row in records}
        _, records = read_table(DATA, 'fee_treasury')
        cash = {row['fact']: row for row in records}
        self.assertLess(int(legs['L1']['order']), int(ops['O1']['order']))
        self.assertLess(int(ops['O1']['known']), int(routes['R1']['seen']))
        self.assertLess(int(cash['K8']['step']), int(routes['R4']['seen']))
        self.assertEqual(cash['K13']['payment'], cash['K15']['payment'])
        self.assertLess(int(cash['K13']['step']), int(cash['K14']['step']))
        self.assertLess(int(cash['K14']['step']), int(cash['K15']['step']))


if __name__ == "__main__":
    unittest.main()
