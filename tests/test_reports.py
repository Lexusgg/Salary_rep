import pytest
from reports import (
    generate_payout_report,
    generate_avg_rate_report,
    generate_report,
    ReportType
)

@pytest.fixture
def sample_employees():
    return [
        {
            'id': '1',
            'email': 'alice@example.com',
            'name': 'Alice Johnson',
            'department': 'Marketing',
            'hours_worked': 160,
            'hourly_rate': 50
        },
        {
            'id': '2',
            'email': 'bob@example.com',
            'name': 'Bob Smith',
            'department': 'Design',
            'hours_worked': 150,
            'hourly_rate': 40
        },
        {
            'id': '3',
            'email': 'carol@example.com',
            'name': 'Carol Williams',
            'department': 'Design',
            'hours_worked': 170,
            'hourly_rate': 60
        }
    ]

def test_generate_payout_report(sample_employees):
    """Test generating payout report."""
    report = generate_payout_report(sample_employees)
    
    assert "Alice Johnson" in report
    assert "Bob Smith" in report
    assert "Carol Williams" in report
    assert "Marketing" in report
    assert "Design" in report
    assert "$8000" in report  # Alice's payout
    assert "$6000" in report  # Bob's payout
    assert "$10200" in report  # Carol's payout

def test_generate_report_payout(sample_employees):
    """Test generating report through main function."""
    report = generate_report(ReportType.PAYOUT.value, sample_employees)
    assert "Alice Johnson" in report

def test_generate_report_invalid_type(sample_employees):
    """Test generating invalid report type."""
    with pytest.raises(ValueError):
        generate_report('invalid', sample_employees)

def test_generate_avg_rate_report(sample_employees):
    """Test generating average rate report."""
    report = generate_avg_rate_report(sample_employees)
    assert "Design" in report
    assert "Marketing" in report
    assert "50.00" in report  # Alice's rate
    # Проверяем правильность расчёта средней ставки для Design
    assert "50.00" in report  # (40 + 60) / 2 = 50

def test_generate_report_avg_rate(sample_employees):
    """Test generating avg_rate report through main function."""
    report = generate_report(ReportType.AVG_RATE.value, sample_employees)
    assert "Design" in report

def test_generate_payout_report_json(sample_employees):
    """Test JSON output for payout report."""
    report = generate_payout_report(sample_employees, output_format='json')
    assert '"department": "Design"' in report
    assert '"total_payout": 16200' in report  # 6000 + 10200
    assert '"payout": 8000' in report  # Alice's payout

def test_generate_avg_rate_report_json(sample_employees):
    """Test JSON output for avg_rate report."""
    report = generate_avg_rate_report(sample_employees, output_format='json')
    assert '"Design": 50.0' in report  # (40 + 60) / 2
    assert '"Marketing": 50.0' in report  # Only Alice