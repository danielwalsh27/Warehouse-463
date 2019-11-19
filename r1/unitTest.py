import unittest
import main

class TestStringMethods(unittest.TestCase):
    def test_1_initial_warehouses(self):
        self.assertEqual(main.warehouses, [])
        
    def test_2_add_warehouse(self):
        main.warehouseWidth.text = 5
        main.warehouseHeight.text = 5
        main.onWarehouseDimensionButtonClicked()
        self.assertEqual(len(main.warehouses), 1)
        self.assertEqual(main.warehouses[0].width, 5)

if __name__ == '__main__':
    main.pg.display.iconify()
    unittest.main()