function makePlot(mat, div_name, plot_type,cbar,hue,smin,smax){  
  try{  
    //x = [0,1,2]
    //y = [0,1,2]
    //mat = [[1,2,3],[3,2,1],[0,-1,5]];

    vmin = 1000;
    vmax = -1000;

    for(var i = 0; i < mat.length; i++) {
      var mata = mat[i];
      for(var j = 0; j < mata.length; j++) {
          vmax = Math.max(vmax,mata[j]);
          vmin = Math.min(vmin,mata[j]);
      }
    }

    //alert(vmin)
    //alert(vmax)

    vmin = vmin * smin/100;
    vmax = vmax * smax/100;

    //alert(vmin)
    //alert(vmax)
    
    var size = (vmax - vmin) / 20;
    var zero_frac = (0 - vmin) / (vmax - vmin);

    cs_scl_gbr = [[0,'Grey'],[zero_frac, 'Snow'], [zero_frac+0.01, 'LightBlue'], [zero_frac+0.2, 'CornflowerBlue'], [0.8, 'Crimson'], [1, 'rgb(100, 0, 0)']];
    cs_scl_bw = [[0, 'Snow'], [1, 'Black']];
    cs_scl_br = [[0, 'CornflowerBlue'], [zero_frac, 'Snow'], [1, 'Crimson']];
    col_bar = {title: "",thickness: 15,len: 0.85,x: +.95}

    if (hue == "GBR"){
      cs_scl = cs_scl_gbr;
    }else if (hue == "BW"){
      cs_scl = cs_scl_bw;
    }else{
      cs_scl = cs_scl_br;
    }
      
    var dataH = [{
      x:[1,2,3,4],
      type:"histogram"
    }];

    var data = [{      
        x:mat[0],
        y:mat[0],
        colorscale: cs_scl, 
        showscale: cbar,
        colorbar: col_bar, 
        z: mat, 
        type: plot_type,          
        line: { width: 0.5, color: 'Gray' },
        name: "XY",
        zmin:vmin,
        zmax:vmax
      }];
    
    var layout = {
        grid: { rows: 1, columns: 1, pattern: 'independent' },
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
      

    Plotly.newPlot(div_name, data,layout,config);    
  }catch(err){
    alert(err.message);
  }
}


