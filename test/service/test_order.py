from unittest.mock import patch

from service.order import CalculateDiscount
from domain.customer import Customer
from domain.product import Money

from test.domain.test_order import create_order_line_helper


class TestCalculateDiscount():
    @patch('service.order.CustomerRepository')
    @patch('service.order.RuleDiscounter')
    def test_calculate_discount(
            self, MockCustomerRepository, MockRuleDiscounter):
        customer_repository = MockCustomerRepository()
        customer_repository.find_by_id.return_value = Customer()
        rule_discounter = MockRuleDiscounter()
        rule_discounter.apply_rules.return_value = Money(100)

        calculate_discount_service = CalculateDiscount(
                customer_repository, rule_discounter)
        order_lines = [create_order_line_helper()]
        result: Money = calculate_discount_service.calculate_discount(
                order_lines, 'customer_id')

        assert result == Money(100)
