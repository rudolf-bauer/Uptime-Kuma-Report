import click

from kumareport.database import Database
from kumareport.chart import chart_plotly


@click.command
@click.option('--tag', '-t', help='Tagname of the monitors to include in the report')
@click.option('--db', help='Uptime Kuma database path.', type=click.File(), required=True)
@click.option('--days', '-d', help='Number of days to report.', type=int, required=True)
def cli(db, days, tag):
    Database(db.name)

    chart = chart_plotly(days, tag)
    chart.show()
