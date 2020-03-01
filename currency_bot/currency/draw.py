# import io
#
#
# # import plotly.graph_objects as go
# #
# # fig = go.Figure(
# #     data=[go.Bar(y=[2, 1, 3])],
# #     layout_title_text="A Figure Displayed with the 'png' Renderer"
# # )
# # fig.show(renderer="jpeg")
#
#
# data = {
#     'rates': {
#         '2020-02-26': {'EUR': 0.9195402299, 'USD': 1.0}, '2020-02-25': {'EUR': 0.9225092251, 'USD': 1.0},
#         '2020-02-24': {'EUR': 0.9243852838, 'USD': 1.0}, '2020-02-27': {'EUR': 0.9120758847, 'USD': 1.0},
#         '2020-02-28': {'EUR': 0.9109957183, 'USD': 1.0}
#     },
#     'start_at': '2020-02-23',
#     'base': 'USD',
#     'end_at': '2020-03-01'
# }
#
#
#
# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
#
# rates = data['rates']
# dates = list(rates.keys())
# currencies = list(rates[dates[0]].keys())
#
# fig = Figure()
# ax = fig.subplots()
#
# # currency = currencies[0]
# for currency in currencies:
#     ax.plot(dates, [1 / rates[date][currency] for date in dates], label=currency)
#
# buffer = io.BytesIO()
# fig.legend()
# fig.savefig(buffer, format='png')
# # plt.close()
#
#
# with open("image.png", "wb") as f:
#     f.write(buffer.getbuffer())
#
#
# # line 1 points
# # x1 = [1, 2, 3]
# # y1 = [2, 4, 1]
# # plotting the line 1 points
# # plt.plot(x1, y1, label="line 1")
#
# # line 2 points
# # x2 = [1, 2, 3]
# # y2 = [4, 1, 3]
# # # plotting the line 2 points
# # plt.plot(x2, y2, label="line 2")
#
# # naming the x axis
# # plt.xlabel('x - axis')
# # naming the y axis
# # plt.ylabel('y - axis')
# # giving a title to my graph
# # plt.title('Two lines on same graph!')
#
# # show a legend on the plot
# # plt.legend()
#
# # function to show the plot
# # plt.show()
