
function makeCross(div_id,slice,min_per, max_per,show_bar){
  try{

        
    cs_proj = [[0, 'Snow'], [0.1, 'LightBlue'], [0.5, 'CornflowerBlue'], [0.9, 'Crimson'], [1, 'rgb(100, 0, 0)']];                    

    col_bar = {title: "",thickness: 15,len: 0.85,x: +.95};
    
    // set up the min and max caps for the visualisation
    vmin = 1000;
    vmax = -1000;
    for(var i = 0; i < slice.length; i++) {
      var mata = slice[i];
      for(var j = 0; j < mata.length; j++) {
          vmax = Math.max(vmax,mata[j]);
          vmin = Math.min(vmin,mata[j]);
      }
    }
    //alert(vmin,vmax)
    vmin = vmin * min_per/100;
    vmax = vmax * max_per/100;
    var f0 = (0 - vmin) / (vmax - vmin);
    var f1 = f0 + ((1-f0)*0.25);
    var f2 = f0 + ((1-f0)*0.5);
    var f3 = f0 + ((1-f0)*0.75);
    if (vmin >= 0){
      cs_scl_gbr = [[0, 'Snow'], [f1, 'LightBlue'], [f2, 'CornflowerBlue'], [f3, 'Crimson'], [1, 'rgb(100, 0, 0)']];
    }else{
      cs_scl_gbr = [[0,'Grey'],[f0, 'Snow'], [f1, 'LightBlue'], [f2, 'CornflowerBlue'], [f3, 'Crimson'], [1, 'rgb(100, 0, 0)']];
    }

    var trace_slice = {            
      colorscale: cs_scl_gbr, 
      showscale: show_bar,
      colorbar: col_bar, 
      z: slice, 
      type: "heatmap",   
      hovertemplate:'......%{z:.4f}',
      zmin:vmin,
      zmax:vmax,
      name:"",
    };
        
    var data = [trace_slice];
                                      
    var layout = {
        grid: { rows: 1, columns: 1, pattern: 'independent' },
        //hovermode:true,
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
    

    Plotly.newPlot(div_id, data,layout,config);    
    //Plotly.newPlot(div_id, [],{},{});    
  
  }catch(err){
    alert("make_cross:" + err.message);
  }
}


