function makePlot(mat, div_name, plot_type,cbar,hue,smin,smax,zero_dotsX,zero_dotsY,posi_dotsX,posi_dotsY,negi_dotsX,negi_dotsY,naybs,vmin,vmax){
  try{      
    // if the plot has no data in there is no point in continuing
    if (mat.length <= 1){      
      return;
    }            
    
    var data_scatter_pos_zero = {        
      x: zero_dotsX,
      y: zero_dotsY,
      hoverinfo:'skip',
      hovertemplate:'',
      mode: 'markers',
      type: "scatter",
      colorscale: [[0, 'rgba(0,0,0,0)'], [1, 'rgba(0, 100, 0,1)']],
      showscale: false,     
      showlegend: false,
      name: "",
      marker: {
          color: 'Gold',
          size: 4,            
      },
    } 
    var data_scatter_pos_posi = {        
      x: posi_dotsX,
      y: posi_dotsY,
      hoverinfo:'skip',
      hovertemplate:'',
      mode: 'markers',
      type: "scatter",
      colorscale: [[0, 'rgba(0,0,0,0)'], [1, 'rgba(0, 100, 0,1)']],
      showscale: false,     
      showlegend: false,
      name: "",
      marker: {
          color: 'cyan',
          size: 4,            
      },
    }
    var data_scatter_pos_negi = {        
      x: negi_dotsX,
      y: negi_dotsY,
      hoverinfo:'skip',
      hovertemplate:'',
      mode: 'markers',
      type: "scatter",
      colorscale: [[0, 'rgba(0,0,0,0)'], [1, 'rgba(0, 100, 0,1)']],
      showscale: false,     
      showlegend: false,
      name: "",
      marker: {
          color: 'lime',
          size: 4,            
      },
    }

    if (div_name == "slice_density"){
      vmin = vmin * smin/100;
      vmax = vmax * smax/100;
    }else{
      vmin = 1000;
      vmax = -1000;
      for(var i = 0; i < mat.length; i++) {
        var mata = mat[i];
        for(var j = 0; j < mata.length; j++) {
            vmax = Math.max(vmax,mata[j]);
            vmin = Math.min(vmin,mata[j]);
        }
      }
    }

    

    //alert(vmin)
    //alert(vmax)

    title_u = ""//"Min="+String(Math.round(vmin*1000)/1000) + " Max="+String(Math.round(vmax*1000)/1000)
    
    

    //alert(vmin)
    //alert(vmax)
        
    var size = (vmax - vmin) / 20;
    var f0 = (0 - vmin) / (vmax - vmin);
    cs_scl_br = [[0, 'Navy'],[0.0001, 'CornflowerBlue'], [f0, 'Snow'], [0.9999, 'Crimson'],[1, 'rgb(100, 0, 0)']];
    cs_scl_rb = [[0, 'rgb(100, 0, 0)'],[0.0001, 'Crimson'], [f0, 'Snow'], [0.9999, 'CornflowerBlue'],[1, 'Navy']];
    
    if (f0 <= 0){
      f0 = 0;
      cs_scl_br = [[0, 'Navy'],[0.0001, 'CornflowerBlue'], [0.5, 'Snow'], [0.9999, 'Crimson'],[1, 'rgb(100, 0, 0)']];
      cs_scl_rb = [[0, 'rgb(100, 0, 0)'],[0.0001, 'Crimson'], [0.5, 'Snow'], [0.9999, 'CornflowerBlue'],[1, 'Navy']];
    }
    var f1 = f0 + ((1-f0)*0.25);
    var f2 = f0 + ((1-f0)*0.5);
    var f3 = f0 + ((1-f0)*0.75);

    cs_scl_gbr = [[0,'Grey'],[f0, 'Snow'], [f1, 'LightBlue'], [f2, 'CornflowerBlue'], [f3, 'Crimson'], [1, 'rgb(100, 0, 0)']];
    cs_scl_bw = [[0, 'Black'], [1, 'Snow']];
    cs_scl_wb = [[0, 'Snow'], [1, 'Black']];
    
    col_bar = {title: title_u,thickness: 15,len: 0.85,x: +.95,titleside:"top"};
    
    if (hue == "BR"){
      cs_scl = cs_scl_br;
    }else if (hue == "RB"){
      cs_scl = cs_scl_rb;
    }else if (hue == "BW"){
      cs_scl = cs_scl_bw;
    }else if (hue == "WB"){
      cs_scl = cs_scl_wb;
    }else{      
      cs_scl = cs_scl_gbr;
    }
        
    
    var annos = [];
    var annosA = naybs.split("[");    
    for (var i = 0; i < annosA.length; i++){
      if (annosA[i].length > 2){
        annosA[i] = annosA[i].replace("[","");
        annosA[i] = annosA[i].replace("]","");        
        annos.push(annosA[i])
      }            
    }
    for (var i = 0; i < annos.length; i++){      
      annos[i] = annos[i].split(",");    
    }
    
    if (annos.length != mat.length){
      var annos = [];
      for (var i = 0; i < mat.length; i++){
        var row = [];
        for (var j = 0; j < mat.length; j++){
          row.push("");
        }
        annos.push(row);
      }
    }
            
    var data_slice = {      
      //x:mat[0],
      //y:mat[0],
      colorscale: cs_scl, 
      showscale: cbar,
      colorbar: col_bar, 
      z: mat, 
      text:annos,   
      hovertemplate:'......%{z:.4f}<br>%{text}',
      hoverlabel:{bgcolor:'rgba(1,1,1,0.05)',align:'left'},     
      type: plot_type,          
      line: { width: 0.5, color: 'Gray' },
      name: "",
      zmin:vmin,
      zmax:vmax,
      contours: {
        start: vmin,
        end: vmax,
        size: size
    },
    }
              
    var data = [data_slice,data_scatter_pos_zero,data_scatter_pos_posi,data_scatter_pos_negi];
    
    var layout = {
        grid: { rows: 1, columns: 1, pattern: 'independent' },
        //hovermode:false,
        autosize: true,
        title: '',
        showlegend: false,
        xaxis: {showgrid: false,zeroline: false,visible: false,},        
        yaxis: {scaleanchor: 'x',scaleratio: 1,visible: false,},      
        margin: {l: 20,r: 80,b: 20,t: 20,pad: 4},
    };

    var config = {
        responsive: true,
        toImageButtonOptions: { scale: 6, width: 540, height: 540 }
    };
      

    Plotly.newPlot(div_name, data,layout,config,{});    
  }catch(err){
    alert("makeplot:" + err.message);
  }
}


