import io
import xlsxwriter


def generate_excel(dataset, by_year, by_country, by_sector):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)

    # Creating worksheet objects
    data_sheet = workbook.add_worksheet(name="Datasheet")
    chart_sheet = workbook.add_worksheet(name="Chartsheet")
    hidden_sheet = workbook.add_worksheet(name="aggregation")

    # configuring formatting
    bold_header_format = workbook.add_format({"bold": True, "align": "center"})
    amount_format = workbook.add_format({"num_format": "€#,##0.00", "align": "left"})
    amount_format_table = workbook.add_format(
        {"num_format": "€#,##0.00", "align": "left", "font_size": 8}
    )
    date_format = workbook.add_format({"num_format": "d-mm-yyyy", "align": "left"})
    dropdown_format = workbook.add_format(
        {"bg_color": "#241E4E", "bold": True, "align": "right", "font_color": "white"}
    )

    # writing the scraped data to Sheet 1 (Datasheet)

    dataset_table = [
        [
            str(data.uid),
            data.title,
            data.country.name,
            data.sector.name,
            data.currency.symbol,
            data.signed_amount,
            data.signature_date,
        ]
        for data in dataset
    ]

    data_sheet.add_table(
        f"A1:G{len(dataset_table)}",
        {
            "data": dataset_table,
            "autofilter": False,
            "columns": [
                {"header": "UID"},
                {"header": "TITLE"},
                {"header": "COUNTRY"},
                {"header": "SECTOR"},
                {"header": "CURRENCY"},
                {"header": "SIGNED AMOUNT", "format": amount_format},
                {"header": "SIGNSTURE DATE", "format": date_format},
            ],
        },
    )

    # Working on Sheet2 (ChartSheet)
    # Dropdown list
    chart_sheet.data_validation(
        "B2",
        {
            "validate": "list",
            "source": ["By Country", "By Year", "By Sector"],
        },
    )
    # Setting default value to the cell
    chart_sheet.write("B2", "By Country", dropdown_format)

    # Adding chart objects
    chart = workbook.add_chart({"type": "column"})
    chart2 = workbook.add_chart({"type": "column"})

    # Preparing data for hidden sheet table to be used for the chart series
    agg_by_year = [
        [data["signature_date__year"], data["total_amount"], data["count"]]
        for data in by_year
    ]
    agg_by_country = [
        [data["country__name"], data["total_amount"], data["count"]]
        for data in by_country
    ]

    agg_by_sector = [
        [data["sector__name"], data["total_amount"], data["count"]]
        for data in by_sector
    ]

    hidden_sheet.add_table(
        f"B1:D{1+len(agg_by_year)}",
        {
            "data": agg_by_year,
            "name": "DataAggregationbyyear",
            "total_row": False,
            "autofilter": False,
            "columns": [
                {"header": "Year"},
                {"header": "Loan Amount", "format": amount_format_table},
                {"header": "Quantity"},
            ],
        },
    )

    hidden_sheet.add_table(
        f"F1:H{1+len(agg_by_country)}",
        {
            "data": agg_by_country,
            "name": "DataAggregationbycountry",
            "autofilter": False,
            "columns": [
                {"header": "Country"},
                {"header": "Loan Amount", "format": amount_format},
                {"header": "Quantity"},
            ],
        },
    )

    hidden_sheet.add_table(
        f"J1:L{1+len(agg_by_sector)}",
        {
            "data": agg_by_sector,
            "name": "DataAggregationbySector",
            "total_row": False,
            "autofilter": False,
            "columns": [
                {"header": "Country"},
                {"header": "Loan Amount", "format": amount_format},
                {"header": "Quantity"},
            ],
        },
    )

    # Creating dynamic data (excel formula) to be used for the chart series as defined names
    chart_y_series = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$G$2:$G${1+len(by_country)},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$C$2:$C${1+len(by_year)},\
                aggregation!$K$2:$K${1+len(by_sector)}\
            )\
        )'
    chart_x_label = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$F$2:$F${1+len(by_country)},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$B$2:$B${1+len(by_year)},\
                aggregation!$J$2:$J${1+len(by_sector)}\
            )\
        )'

    chart2_y_series = f'=IF(Chartsheet!$B$2="By Country",\
        aggregation!$H$2:$H${1+len(by_country)},\
            IF(Chartsheet!$B$2="By Year",\
                aggregation!$D$2:$D${1+len(by_year)},\
                aggregation!$L$2:$L${1+len(by_sector)}\
            )\
        )'

    # defining names that can be used to represent excel functions and formulas: returns range of cells
    workbook.define_name("chart_series", chart_y_series)
    workbook.define_name("chart_labels", chart_x_label)
    workbook.define_name("chart2_series", chart2_y_series)
    workbook.define_name("chart2_labels", chart_x_label)

    # Adding chart series (y-axis values as 'values' and x-axis values as 'categories')
    chart.add_series(
        {
            "values": "=aggregation!chart_series",
            "categories": "=aggregation!chart_labels",
            "fill": {"color": "#FF9900"},
        }
    )

    chart2.add_series(
        {
            "values": "=aggregation!chart2_series",
            "categories": "=aggregation!chart2_labels",
            "fill": {"color": "#FF9900"},
        }
    )

    # setting addition info
    chart.set_size({"width": 720})
    chart.set_title({"name": "Total Loan Amount"})
    chart2.set_legend({"none": True})
    chart.set_style(30)
    chart2.set_size({"width": 720})
    chart2.set_title({"name": "Total Loan Quantity"})
    chart.set_legend({"none": True})
    chart2.set_style(30)

    # Inserting the charts into the chart sheet
    chart_sheet.insert_chart("B4", chart)
    chart_sheet.insert_chart("B20", chart2)

    # auto fitting the cells to the width of the contents
    chart_sheet.autofit()
    data_sheet.autofit()

    # Hide the sheet
    hidden_sheet.hide()

    workbook.close()
    output.seek(0)

    return output
