import unittest
import main

class TestStringMethods(unittest.TestCase):
    def test_1_initial_warehouses(self):
        print("Testing Null Warehouse List")
        self.assertEqual(main.warehouses, [])
        print("Test 1 PASS")
        
    def test_2_add_warehouse(self):
        print("Testing Add Warehouse")
        main.warehouseWidth.text = 5
        main.warehouseHeight.text = 5
        main.onWarehouseDimensionButtonClicked()
        self.assertEqual(len(main.warehouses), 1)
        self.assertEqual(main.warehouses[0].width, 5)
        main.warehouses = []
        main.warehouseHeight.text = ""
        main.warehouseWidth.text = ""
        print("Test 2 PASS")

if __name__ == '__main__':
    main.pg.display.iconify()
    unittest.main()