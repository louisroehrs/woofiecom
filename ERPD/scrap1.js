           // the inner layout houses the grid panel and the preview panel
            var innerLayout = new Ext.BorderLayout.create({
                north: {
                    height: 32,
                    fitToFrame: true,
                    autoCreate: true
                },
				east: {
					panels: [new Ext.ContentPanel('vrpd-usage',{ 
  			            fitToFrame: true,
 			            autoCreate: true,})],
                    fitToFrame: true,
                    autoScroll: false,
					initialSize: 200,

					
				},
                center: {
                    margins: {
                        left: 3,
                        top: 3,
                        right: 3,
                        bottom: 3
                    },
                    panels: [new Ext.GridPanel(grid)],
					initialSize:250,
					minSize:250

                }
            }, 'channels');
            