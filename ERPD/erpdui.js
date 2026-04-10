/*
 *
 * Copyright(c) 2006-2007=8
 * licensing@extjs.com
 *
 * http://www.extjs.com/license
 */

Ext.BLANK_IMAGE_URL = "images/s.gif";  // makes things go much faster.

var ERPD = function(){
    // common layouts and panels
  var layout, statusPanel, rightPanel,navPanel, updateForm;

    // panels for tabs
  var vrpdsPanel, channelsPanel, operationsPanel, externalNetworkPanel, systemPanel;

    // status panels
    var operationsStatusPanel,externalNetworkStatusPanel, systemStatusPanel;

    // addtional special panels
  var vrpdUsagePanel;

    var ERPDtoolbar;
    // channel grid and store

    var channelGrid, channelDS, channelCM;
    // vrpd grid and store

    var vrpdGrid, vrpdDS, vrpdCM;
    var seed = 0;
    // data objects
    var Channel, VRPD;
    
    // icon text strings for buttons.
    var stopDemodText = "<img src='images/default/menu/checked.gif' align=top>&nbsp;&nbsp;Stop Demodulation";
    var startDemodText = "<img src='images/default/menu/unchecked.gif' align=top>&nbsp;&nbsp;Start Demodulation";
    
    var stopNetworkText = "<img src='images/default/menu/checked.gif' align=top>&nbsp;&nbsp;Stop Network";
    var startNetworkText = "<img src='images/default/menu/unchecked.gif' align=top>&nbsp;&nbsp;Start Network";
    
    var noFrontendText = "<img src='images/default/menu/checked.gif' align=top>&nbsp;&nbsp;Don't use RF Frontend";
    var useFrontendText = "<img src='images/default/menu/unchecked.gif' align=top>&nbsp;&nbsp;Use RF Frontend";
    
    function formatBoolean(value){
        return value ? 'Yes' : 'No';  
    };

    // System calls
    function onHalt(item){
      Ext.MessageBox.confirm('Confirm', 'Are you sure you want to '+item.text.toLowerCase() + ' the system?',doHalt);
    }

    function doHalt(item) {
      alert(item)
      if (item.toLowerCase()=="yes") {
         systemStatusPanel.load(phppath+'HaltSystem.php' + phpsuffix);
      }
    }

    function doRestart(item) {
      if (item.toLowerCase()=="yes") {
         systemStatusPanel.load(phppath+'RestartSystem.php' + phpsuffix);
      }
    }

    function onReboot(item){
      Ext.MessageBox.confirm('Confirm', 'Are you sure you want to '+item.text.toLowerCase() + ' the system?',doRestart);
    }
    
    // functions to display feedback
    function onButtonClick(btn){
        Ext.example.msg('Button Click', 'You clicked the "{0}" button.', btn.text);
    }
    
    function onClick(item){
        Ext.example.msg('Menu Click', 'You clicked the "{0}" menu item.', item.text);
    }
    
    function onItemCheck(item, checked){
        Ext.example.msg('Item Check', 'You {1} the "{0}" menu item.', item.text, checked ? 'checked' : 'unchecked');
    }
    
    // Operations toolbar actions
    
    function onDemodToggle(item){
        if (item.pressed) {
            operationsStatusPanel.load(phppath+'StartERPD.php'+phpsuffix)
            item.setText(stopDemodText);
        }
        else {
            operationsStatusPanel.load(phppath+'StopERPD.php'+phpsuffix)
            item.setText(startDemodText);
        }
    }

    function onFrontendToggle(item){
        if (item.pressed) {
            item.setText(noFrontendText);
        }
        else {
            item.setText(useFrontendText);
        }
    }
    
    function onDemodRestart(item){
        operationsStatusPanel.load(phppath+'RestartERPD.php'+phpsuffix)
    }
    
    function onDemodStatus(item){
        operationsStatusPanel.load(phppath+'ShowStatus.php'+phpsuffix)
    }
    
    function onDemodBackup(item){
        operationsStatusPanel.load(phppath+'BackupConfigFile.php'+phpsuffix)
    }
    
    function onDemodRestore(item){
        operationsStatusPanel.load(phppath+'RestoreConfigFile.php'+phpsuffix)
    }
    
    function onDemodView(item){
        operationsStatusPanel.load(phppath+'ShowConfigFile.php'+phpsuffix+'?filename=data.xml')
    }
	
    function onRightConfigView (item){
		rightPanel.load(phppath + 'ShowConfigFile.php' + phpsuffix + '?filename=data.xml');
		layout.getRegion('east').expand();
	}
	    
    // External network actions
    function onNetworkToggle(item){
        if (item.pressed) {
            externalNetworkStatusPanel.load(phppath+'StartNet.php'+phpsuffix)
            item.setText(stopNetworkText);
        }
        else {
            externalNetworkStatusPanel.load(phppath+'StopNet.php'+phpsuffix)
            item.setText(startNetworkText);
        }
    }
    function onNetworkStatus(item){
      externalNetworkStatusPanel.load(phppath + 'ShowNetStatus.php' + phpsuffix);
    }

    function onNetworkSetup(item){
      externalNetworkStatusPanel.load(phppath + 'ExtNetSetup.php' + phpsuffix);
    }

    function onNetworkSetupSave(item){
      externalNetworkStatusPanel.load(phppath + 'ExtNetSetup.php' + phpsuffix);
    }

  // VRPD GRID handlers

  function doSaveVrpds(item) {
    var data = [];
    modifiedRecords = vrpdGrid.getDataSource().getModifiedRecords();
    for(i=0;i<modifiedRecords.length;i++) {
      data.push(modifiedRecords[i].data);
    }
    dataString= Ext.encode(data);
    alert(dataString);
    statusPanel.load({url:phppath+'SaveVrpds.php' + phpsuffix,params:{gridMods:dataString}});

    //    var mgr = statusPanel.getEl().getUpdateManager();
    
    //    mgr.update({url:phppath+'SaveVrpds.php' + phpsuffix,params:{gridMods: dataString}});
  }

    function onAddVRPD (item){
        var v = new VRPD({
          vrpd: vrpdDS.getCount()+1,
          name: '',
          ipaddr: 0,
          sport: 1024,
          nc1500: '',
              dport: '',
          idle_tx: false
              });
        vrpdGrid.stopEditing();
        vrpdDS.insert(0, v);
        vrpdGrid.startEditing(0, 0);
    }


	    
    function doNav(sm, n){
        if (n) {
            layout.getRegion("center").showPanel(n.id);
        }
    }
    
    return {
        init: function(){
            // create the main layout
            layout = new Ext.BorderLayout(document.body, {
                north: {
                    split: false,
                    initialSize: 50,
                    titlebar: false
                },
                west: {
                    split: true,
                    initialSize: 150,
                    minSize: 150,
                    maxSize: 200,
                    titlebar: true,
                    collapsible: true,
                    animate: true,
                    autoScroll: false,
                    useShim: true,
                    cmargins: {
                        top: 0,
                        bottom: 2,
                        right: 2,
                        left: 2
                    }
                },
                east: {
                    split: true,
                    initialSize: 400,
                    minSize: 175,
                    maxSize: 800,
                    titlebar: true,
                    collapsible: true,
                    animate: true,
                    autoScroll: true,
                    useShim: true,
                    collapsed: true,
                    cmargins: {
                        top: 0,
                        bottom: 2,
                        right: 2,
                        left: 2
                    }
                },
                south: {
                    split: true,
                    initialSize: 24,
                    minsize: 24,
                    titlebar: false,
                    collapsible: false,
                    animate: false
                },
                center: {
                    titlebar: false,
                    title: "Demodulation Configuration",
                    autoScroll: false,
                    tabPosition: 'top',
                    alwaysShowTabs: false
                }
            });
            // tell the layout not to perform layouts until we're done adding everything
            layout.beginUpdate();
            layout.add('north', new Ext.ContentPanel('header'));

            
            // initialize the bar
            statusPanel = new Ext.ContentPanel('status',{ 
              fitToFrame: true,
              autoScroll: true});
            updateForm = new Ext.form.BasicForm('updateForm');

            south = layout.getRegion('south');
            south.add(statusPanel);
            
			rightPanel =new Ext.ContentPanel('rightpanel', {
                title: 'Configuration',
                fitToFrame: true,
				autoScroll: true
            })
            layout.add('east', rightPanel );
            
            
            ERPDtoolbar = this.createDemodToolbar('ERPDtoolbar');

            this.createOperationsPanel();
            this.createVrpdUsagePanel();	
            this.createVrpdPanel();	
            this.createChannelsPanel();
            this.createStatisticsPanel();
            this.createNetworkPanel();
            this.createSystemPanel();

            // Create Support Panel
            var support = layout.add('center', new Ext.ContentPanel('support', {
                id: 'support',
                title: 'Support',
                fitToFrame: true,
                autoScroll: true,
                autoCreate: false,
                url: 'support.php'
            }));
            // restore any state information
            layout.restoreState();
            
            this.createNav();
            layout.getRegion('center').showPanel('operations');
            layout.endUpdate();

            this.raiseCurtain();
        },
        
        raiseCurtain: function() {
			var loading = Ext.get('loading');
			var mask = Ext.get('loading-mask');
			mask.setOpacity(.8);
			mask.fadeOut({duration:.1,remove:true});
            loading.fadeOut({duration:.1,remove:true});
         },

        createVrpdUsagePanel: function () {
            vrpdUsagePanel = new Ext.ContentPanel('vrpd-usage',{ 
              fitToFrame: true,
              autoCreate: true})
        },
    
        createDemodToolbar: function(element){
            ERPDtoolbar = new Ext.Toolbar(element, [{
                id: 'demodbutton',
                text: startDemodText, // LFR get current state
                handler: onDemodToggle,
                enableToggle: true,
                cls: 'x-btn-text',
                tooltip: 'Start or stop the demodulation service.'
            }, {
                text: 'Restart',
                handler: onDemodRestart,
                cls: 'x-btn-text',
                tooltip: 'Restart the demodulation service.'
            }, '-', {
                text: 'View Status',
                handler: onDemodStatus,
                cls: 'x-btn-text',
                tooltip: 'View status of the demodulation service.'
            }, '-', {
                text: 'Backup Configuration',
                handler: onDemodBackup,
                icon: 'images/new_window.gif',
                cls: 'x-btn-text'
            }, {
                text: 'Restore Configuration',
                handler: onDemodRestore,
                icon: 'images/new_window.gif',
                cls: 'x-btn-text'
            }, {
                text: 'View Configuration File',
                handler: onDemodView,
                cls: 'x-btn-text'
            }]);
            return ERPDtoolbar;
            
        },
        
        createOperationsPanel: function(){
            // the inner layout houses the toolbar and response panel 
            var innerLayout = new Ext.BorderLayout.create({
                north: {
                    initialSize: 27,
                    fitToFrame: true
                },
                center: {
                    fitToFrame: true
                }
            }, 'operations');
            
            operationsStatusPanel = innerLayout.add('center', new Ext.ContentPanel('operationsstatus', {
                fitToFrame: true,
                autoCreate: true,
                autoScroll: true
            }));
            
            innerLayout.add('north', new Ext.ContentPanel('operationssheader', {
                fitToFrame: true,
                id: 'operationssheader',
                autoCreate: true
            }));
            
            operationsPanel = new Ext.NestedLayoutPanel(innerLayout, {
                title: 'Operations',
                fitToFrame: true
            });
            
            ERPDtoolbar = this.createDemodToolbar(innerLayout.getRegion('north').getEl());
            
            layout.add('center', operationsPanel);
            
        },

        createVrpdPanel: function () {
            var Grid = Ext.grid;
            var Form = Ext.form;
            var Ed = Ext.grid.GridEditor;
            // the column model has information about grid columns
            // dataIndex maps the column to the specific data field in
            // the data store (created below)
            var vrpdCM = new Ext.grid.ColumnModel([
              {
                header: "vRPD",
                dataIndex: 'vrpd',
                width: 50,
                sortable: true,
                align: 'right',
                locked: true

              }, 
              {                  /*     name="mojo1-2.oamp.mp.agile.tv" */
                header: "Name",
                dataIndex: 'name',
                width: 200,
                align: 'right',
                editor: new Ed(new Form.TextField({allowBlank:false}))
              }, 
              {   //    ipaddr="172.16.0.31/24"
                header: "IP Address/Bits",
                dataIndex: 'ipaddr',
                width: 110,
                align: 'right',
                editor: new Ed(new Form.TextField({allowBlank:false}))
              },
              {   //    sport="1024"
                header: "Port",
                dataIndex: 'sport',
                width: 40,
                align: 'right',
                editor: new Ed(new Form.NumberField(
                                                    {allowBlank:false,
                                                        allowNegative:false,
                                                        maxValue: 65536}))
              },
              {   //    ipaddr="172.16.0.31"
                header: "NC-1500 IP Address",
                dataIndex: 'nc1500',
                width: 110,
                align: 'right',
                editor: new Ed(new Form.TextField({allowBlank:false}))
              },
              {   //    dport="1024"
                header: "Port",
                dataIndex: 'dport',
                width: 40,
                align: 'right',
                editor: new Ed(new Form.NumberField(
                                                    {allowBlank:false,
                                                        allowNegative:false,
                                                        maxValue: 65536}))
              },
              {
                header: "Idle TX",
                dataIndex: 'idle_tx',
                renderer: formatBoolean,
                width: 60,
                align: 'right',
                  editor: new Ed(new Form.Checkbox({autoCreate:true}))
              }
              ]);



            
            // by default columns are sortable
            vrpdCM.defaultSortable = true;
            
            VRPD = Ext.data.Record.create([ // the "name" below matches the tag name to read, except "availDate"
            // which is mapped to the tag "availability"
              {
                name: 'vrpd', type: 'number'
              },
              {
                name: 'name', type: 'string'
              },
              {
                name: 'ipaddr', type: 'string'
              },
              {
                name: 'sport', type: 'string'
              },
              {
                name: 'nc1500', type: 'string'
              },
              {
                name: 'dport', type: 'string'
              },
              {
                name: 'idle_tx', type: 'boolean'
              }
              ]);

            vrpdDS = new Ext.data.JsonStore({
              fields: ['vrpd','name','ipaddr','sport','nc1500','dport','idle_tx'],
                  url:(phppath+'LoadVrpds.php'+phpsuffix),
                root: "vrpdList",                // The property which contains an Array of row objects
                  });

            // create the editor grid
            vrpdGrid = new Ext.grid.EditorGrid('vrpdeditor-grid', {
                ds: vrpdDS,
                cm: vrpdCM,
                enableColLock: false,
                autoCreate: true,
                autoScroll: true,
                clicksToEdit:1,
                stripeRows:false
            });
            
            
            // the inner layout houses the grid panel and the preview panel
            var innerLayout = new Ext.BorderLayout.create({
                /*				east: {
                panels: [vrpdUsagePanel],
                    fitToFrame: true,
                    autoScroll: false,
					initialSize: 200
                    }, */
                center: {
                    margins: {
                        left: 3,
                        top: 3,
                        right: 3,
                        bottom: 3
                    },
                    panels: [new Ext.GridPanel(vrpdGrid,{fitToFrame:true, clicksToEdit:1})],
                    fitToFrame: true,
					initialSize:350,
					minSize:250
                    }
            }, 'vrpds');
            
            vrpdsPanel = new Ext.NestedLayoutPanel(innerLayout, {
                title: 'vRPDs',
                fitToFrame: true,
                autocreate:true
            });

            // add the nested layout
            
            layout.add('center', vrpdsPanel);
            
            // render it
            vrpdGrid.render();
            
            var gridHead = vrpdGrid.getView().getHeaderPanel(true);
            var tb = new Ext.Toolbar(gridHead, [
              {
                text: 'Save',
                handler: doSaveVrpds
            },
              {
                text: 'Add vRPD',
                handler: onAddVRPD
            },
              '-', 
			/*  RF Frontend not for shipment.
			{
                text: useFrontendText,
                handler: onFrontendToggle,
                enableToggle: true
            }, 
            */
			{
                text: 'View Configuration File',
                handler: onRightConfigView,
                cls: 'x-btn-text'
            }]);
            
            // trigger the data store load
            
            vrpdDS.load();
            
            // restore innerLayout state
      },

        // keep
        createChannelsPanel: function(){
            var Grid = Ext.grid;
            var Form = Ext.form;
            var Ed = Ext.grid.GridEditor;
            // the column model has information about grid columns
            // dataIndex maps the column to the specific data field in
            // the data store (created below)
            channelCM = new Ext.grid.ColumnModel([{
                header: "Channel",
                dataIndex: 'channel',
                align: 'right',
                width: 150
            }, {
                header: "vRPD",
                dataIndex: 'vrpd',
                width: 50,
                align: 'right',
                editor: new Ed(new Ext.form.ComboBox({
                    typeAhead: true,
                    triggerAction: 'all',
                    transform: 'vrpd-select',
                    lazyRender: true,
                    forceSelection: true
                }))
            }, {
                header: "Port",
                dataIndex: 'port',
                width: 50,
                align: 'right',
                editor: new Ed(new Ext.form.ComboBox({
                    typeAhead: true,
                    triggerAction: 'all',
                    transform: 'port-select',
                    lazyRender: true,
                    forceSelection: true
                }))
             }, {
                header: "Performance",
                dataIndex: 'performance',
                width: 80,
                align: 'left',
                editor: new Ed(new Ext.form.ComboBox({
                    typeAhead: true,
                    triggerAction: 'all',
                    transform: 'perf-select',
                    lazyRender: true,
                    forceSelection: true
                }))
             }, {
                header: "Error Correction",
                dataIndex: 'errorcorrection',
                align: 'left',
                renderer: formatBoolean,
                width: 120,
                align: 'right',
                editor: new Ed(new Form.Checkbox({autoCreate:true}))
                                                  }]);


            
            // by default columns are sortable
            channelCM.defaultSortable = true;
            
            // this could be inline, but we want to define the Plant record
            // type so we can add records dynamically
            var Channel = Ext.data.Record.create([ // the "name" below matches the tag name to read, except "availDate"
            // which is mapped to the tag "availability"
            {
                name: 'channel',
                type: 'string'
            }, {
                name: 'vrpd',
                type: 'string'
            }, {
                name: 'port',
                type: 'string'
            },{
                name: 'performance',
                type: 'string'
            }, {
                name: 'errorcorrection',
                type: 'boolean'
            }]);
            
            
            var freqArray = [];
            var beginFreq = 8.192;
            var incFreq = .256;
            for (i = 1; i <33; i++) {
                freqArray[freqArray.length] = [Math.floor(beginFreq * 1000) / 1000 + ' ',Math.floor(i/6)+' '  ,i%6+' '];
                beginFreq += incFreq;
            }
            channelDS = new Ext.data.JsonStore({
              fields: ['channel', 'vrpd', 'port','performance','errorcorrection'],
                  url:(phppath+'LoadChannels.php'+phpsuffix),
                root: "channelList",                // The property which contains an Array of row objects
            });
                        
            // create the editor grid
            channelGrid = new Ext.grid.EditorGrid('channels-editor-grid', {
                ds: channelDS,
                cm: channelCM,
                enableColLock: false,
                autoCreate: true,
                autoScroll: true,
                clicksToEdit:1,
                stripeRows:false
            });
            
            // the inner layout houses the grid panel and the preview panel
            var innerLayout = new Ext.BorderLayout.create({
                north: {
                    height: 32,
                    fitToFrame: true,
                    autoCreate: true
                },
				east: {
                    panels: [vrpdUsagePanel],
                    fitToFrame: true,
                    autoScroll: false,
					initialSize: 200
				},
                center: {
                    margins: {
                        left: 3,
                        top: 3,
                        right: 3,
                        bottom: 3
                    },
                    panels: [new Ext.GridPanel(channelGrid)],
					initialSize:250,
					minSize:250
                }
            }, 'channels');
            
            innerLayout.add('north', new Ext.ContentPanel('channelsheader', {
                title: 'hey',
                fitToFrame: true,
                id: 'channelsheader',
                height: 150,
                autoCreate: true
            
            }));
            
            channelsPanel = new Ext.NestedLayoutPanel(innerLayout, {
                title: 'Channels',
                fitToFrame: true
            });
            
            // render it
            channelGrid.render();
            
            var gridHead = channelGrid.getView().getHeaderPanel(true);
            var tb = new Ext.Toolbar(gridHead, [{
                text: 'Save'
            }, '-', 

			{
                text: useFrontendText,
                handler: onFrontendToggle,
                enableToggle: true
            }, 

			{
                text: 'View Configuration File',
                handler: onRightConfigView,
                cls: 'x-btn-text'
            }]);
            
            //            var combo = new Ext.form.ComboBox({
            //                typeAhead: true,
            //                transform: 'ERPDPort-select',
            //                triggerAction: 'all',
            //                forceSelecion: true,
            //                selectOnFocus: true,
            //                width: 135
            //            });
            // tb.addField(combo);
            //         tb.addElement("<B>RF Input:&nbsp;&nbsp;</B><select><option>Board 1 Slot 1</option><option>Board 1 Slot 2</option><option>Board 2 Slot 1</option><option>Board 2 Slot 2</option></select>");
            // trigger the data store load
            
            channelDS.load();
            //   innerLayout.endUpdate();
            layout.add('center', channelsPanel);
            
        },

        createStatisticsPanel : function () {
            var statistics = layout.add('center', new Ext.ContentPanel('statistics', {
                id: 'statistics',
                title: 'Statistics',
                fitToFrame: true,
                autoScroll: true,
                autoCreate: true,
                url: 'ERPDstatistics.php'
            }));
        },

        createNetworkPanel: function () {
            // the inner layout houses the toolbar and response panel 
            var innerLayout = new Ext.BorderLayout.create({
                north: {
                    initialSize: 27,
                    fitToFrame: true
                },
                center: {
                    fitToFrame: true
                }
            }, 'externalnetwork');
            
            externalNetworkStatusPanel = innerLayout.add('center', new Ext.ContentPanel('externalnetworkstatus', {
                fitToFrame: true,
                autoCreate: true,
                autoScroll: true,
                url: (phppath +'ExtNetSetup.php' + phpsuffix)                                                                                            
            }));
            
            innerLayout.add('north', new Ext.ContentPanel('externalnetworkheader', {
                fitToFrame: true,
                toolbar: externalNetworkToolbar,
                id: 'externalnetworkheader',
                autoCreate: true
            }));
            
            var externalNetworkToolbar = new Ext.Toolbar(innerLayout.getRegion('north').getEl(), 
            [{
                id: 'extnetworkbutton',
                text: startNetworkText, // LFR get current state
                handler: onNetworkToggle,
                enableToggle: true,
                cls: 'x-btn-text',
                tooltip: 'Start or stop the external network service.'
            }, {
                text: 'View Status',
                handler: onNetworkStatus,
                cls: 'x-btn-text',
                tooltip: 'View status of the external network service.'
            },'-',
              {
                text: 'Setup',
                handler: onNetworkSetup,
                cls: 'x-btn-text',
                tooltip: 'View and modify external network setup.'
              },
              {
                text: 'Save',
                handler: onNetworkSetupSave,
                cls: 'x-btn-text',
                tooltip: 'View and modify external network setup.'
              }
            ]);

            externalNetworkPanel = new Ext.NestedLayoutPanel(innerLayout, {
                title: 'External Network',
                fitToFrame: true
            });
            
            layout.add('center', externalNetworkPanel);

      },

        createSystemPanel: function () {
            // the inner layout houses the toolbar and response panel 
            var innerLayout = new Ext.BorderLayout.create({
                north: {
                    initialSize: 27,
                    fitToFrame: true
                },
                center: {
                    fitToFrame: true
                }
            }, 'system');
            
            systemStatusPanel = innerLayout.add('center', new Ext.ContentPanel('systemstatus', {
                fitToFrame: true,
                autoCreate: true,
                autoScroll: true
            }));
            
            innerLayout.add('north', new Ext.ContentPanel('systemheader', {
                fitToFrame: true,
                id: 'systemheader',
                autoCreate: true
            }));
            
            var systemToolbar = new Ext.Toolbar(innerLayout.getRegion('north').getEl(), [{
                id: 'systemhaltbutton',
                text: 'Halt', // LFR get current state
                handler: onHalt,
                
                cls: 'x-btn-text',
                tooltip: 'Halt the entire box.'
            }, {
                text: 'Restart',
                handler: onReboot,
                cls: 'x-btn-text',
                tooltip: 'Reboot the box'
            }]);

            systemPanel = new Ext.NestedLayoutPanel(innerLayout, {
                title: 'System',
                fitToFrame: true
            });
            
            layout.add('center', systemPanel);

      },

        createNav: function(){
            var Tree = Ext.tree;
            var albums = layout.getEl().createChild({
                tag: 'div',
                id: 'albums'
            });
            var viewEl = albums.createChild({
                tag: 'div',
                id: 'folders'
            });
            
            var folders = layout.add('west', new Ext.ContentPanel(albums, {
                title: 'Contents',
                fitToFrame: true,
                autoScroll: true,
                autoCreate: true,
                resizeEl: viewEl
            }));
            
            
            var tabs = layout.getRegion('center').getTabs();
            var tabnames = "";
            for (var tab in tabs.items) {
                tabnames += ":" + tab;
            }
            //            statusPanel.setContent(tabnames)
            //tabs.hideTab('main');
            //tabs.hideTab('VPRD');
            //tabs.hideTab('images32');
            
            
            
            var tree = new Tree.TreePanel(viewEl, {
                animate: true,
                enableDD: false,
                containerScroll: true,
                rootVisible: false
            });
            tree.getSelectionModel().addListener('selectionchange', doNav, this);
            
            var root = new Tree.TreeNode({
                text: 'Navigation',
                allowDrag: false,
                allowDrop: false
            });
            tree.setRootNode(root);
            
            demod = new Tree.TreeNode({
                text: 'Demodulation',
                cls: 'album-node',
                allowDrag: false,
                id: 'demod'
            });
            
            root.appendChild(demod, new Tree.TreeNode({
                text: 'Statistics',
                cls: 'album-node',
                allowDrag: false,
                id: 'statistics'
            }), new Tree.TreeNode({
                text: 'External Network',
                cls: 'album-node',
                allowDrag: false,
                id: 'externalnetwork'
            }), new Tree.TreeNode({
                text: 'System',
                cls: 'album-node',
                allowDrag: false,
                id: 'system'
            }), new Tree.TreeNode({
                text: 'Support',
                cls: 'album-node',
                allowDrag: false,
                id: 'support'
            }));
            demod.appendChild(new Tree.TreeNode({
                text: 'Operations',
                cls: 'album-node',
                allowDrag: false,
                id: 'operations'
            }), new Tree.TreeNode({
                text: 'vRPDs',
                cls: 'album-node',
                allowDrag: false,
                id: 'vrpds'
            }), new Tree.TreeNode({
                text: 'Channels',
                cls: 'album-node',
                allowDrag: false,
                id: 'channels'
            
            }));
            
            tree.render();
            root.expand();
            demod.expand();
            
            tree.setRootNode(root);
            
        },
        
        
        createView: function(el){
            function reformatDate(feedDate){
                var d = new Date(Date.parse(feedDate));
                return d ? d.dateFormat('D M j, Y, g:i a') : '';
            }
            
            var reader = new Ext.data.XmlReader({
                record: 'item'
            }, ['title', {
                name: 'pubDate',
                type: 'date'
            }, 'link', 'description']);
            
            ds = new Ext.data.Store({
                proxy: new Ext.data.HttpProxy({
                    url: 'feed-proxy.php'
                }),
                reader: reader
            });
            
            //			var RecordDef = Ext.data.Record.create([
            //   			{name: 'name', mapping: 1},         // "mapping" only needed if an "id" field is present which
            //    			{name: 'occupation', mapping: 2}    // precludes using the ordinal position as the index.
            //			]);
            //		var myReader = new Ext.data.ArrayReader({
            // 				 id: 0                     // The subscript within row Array that provides an ID for the Record (optional)
            //			}, RecordDef);
            
            ds.on('load', this.onLoad, this);
            
            var tpl = new Ext.Template('<div class="feed-item">' +
            '<div class="item-title">{title}</div>' +
            '<div class="item-date">{date}</div>' +
            '{desc}</div>');
            
            var view = new Ext.View(el, tpl, {
                store: ds,
                singleSelect: true,
                selectedClass: 'selected-article'
            });
            view.prepareData = function(data){
                return {
                    title: data.title,
                    date: reformatDate(data.pubDate),
                    desc: data.description.replace(/<\/?[^>]+>/gi, '').ellipse(350)
                
                };
            };
            view.on('click', this.showPost, this);
            view.on('dblclick', this.showFullPost, this);
        }
        
        
    }
    
}
();

Ext.onReady(ERPD.init, ERPD);
