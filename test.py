		if self.comboBox_13.currentText() != self.comboBox_12.currentText() and self.comboBox_13.currentText() != self.comboBox_11.currentText() and self.comboBox_12.currentText() != self.comboBox_11.currentText():
			technology_all = {'K線及均線':self.Kline_line,'布林通道':self.bool_line,'KD':self.KD_line,'成交量':self.bar,'RSI':line_RSI,'MACD':self.MACD}
			if self.webEngineView.geometry().width() < 700:
				grid_chart = Grid(init_opts=opts.InitOpts(width="1500px", height="700px"))
			else:
				grid_chart = Grid(init_opts=opts.InitOpts(width=str(self.webEngineView.geometry().width()) + "px", height=str(self.webEngineView.geometry().height()-50) + "px"))
			opendata = list()
			closedata = list()
			for opens in self.open_pr_market[-180:]:
				opendata.append(float(opens))
			for close in self.close_pr_market[-180:]:
				closedata.append(float(close))
			grid_chart.add_js_funcs("var openData = {}".format(opendata))
			grid_chart.add_js_funcs("var closeData = {}".format(closedata))
			grid_chart.add_js_funcs("var stock_info = ''")
			grid_chart.add_js_funcs("""
			document.addEventListener("DOMContentLoaded", function(){
				new QWebChannel(qt.webChannelTransport, function(channel){
					window.bridge = channel.objects.bridge;
				})
			})
			function bitch(){
				if (window.bridge){
					window.bridge.strValue = stock_info;
				}
			}
			document.body.onmousemove = bitch;
			""")
					
			if (self.comboBox_13.currentText() == "布林通道"):
				self.comboBox_11.setDisabled(True)
				grid_chart.add(
					technology_all[self.comboBox_14.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_top='1%',height="34%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_13.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='28%', height="34%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_12.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='9%', height="17%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_11.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='-100%', height="0%"),
				)				
			else:
				opendata = list()
				closedata = list()
				for opens in self.open_pr_market[-180:]:
					opendata.append(float(opens))
				for close in self.close_pr_market[-180:]:
					closedata.append(float(close))
				grid_chart.add_js_funcs("var openData = {}".format(opendata))
				grid_chart.add_js_funcs("var closeData = {}".format(closedata))
				grid_chart.add_js_funcs("var stock_info = ''")
				grid_chart.add_js_funcs("""
				document.addEventListener("DOMContentLoaded", function(){
					new QWebChannel(qt.webChannelTransport, function(channel){
						window.bridge = channel.objects.bridge;
					})
				})
				function bitch(){
					if (window.bridge){
						window.bridge.strValue = stock_info;
					}
				}
				document.body.onmousemove = bitch;
				""")
				
				grid_chart.add(
					technology_all[self.comboBox_14.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_top='1%',height="34%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_13.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='45.5%', height="16%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_12.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='27%', height="16%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_11.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='9%', height="16%",pos_left='4%',pos_right='10'),
				)
				self.comboBox_11.setDisabled(False)
			grid_chart.render("render_Market.html")
			with open('./render_Market.html','r') as f:
				html = f.read()
			soup = BeautifulSoup(html,'html.parser')
			new_tag = soup.new_tag('script', src='./qwebchannel.js')
			soup.head.insert(0,new_tag)
			with open('./render_Market.html','w') as f:
				html = f.write(str(soup))
		else:
			pass
        self.webEngineView.setUrl(QtCore.QUrl("file:///render_Market.html"))
        self.verticalLayout.addWidget(self.webEngineView)
        self.thread = MarketThread()
        self.thread.start()
        self.thread.trigger.connect(self.addinfo)