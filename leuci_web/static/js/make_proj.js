
function makeProjection(proj_xy,atoms_x,atoms_y,atoms_v,div_id,proj,atoms,min_per, max_per,x_ax,y_ax){
  try{
    //alert(proj + " " + atoms)  
    
    cs_atoms = [[0, 'PaleGoldenrod'],[0.5,'Goldenrod'], [1, 'Black']];
    cs_proj = [[0, 'Snow'], [0.1, 'LightBlue'], [0.5, 'CornflowerBlue'], [0.9, 'Crimson'], [1, 'rgb(100, 0, 0)']];                    

    // set up the min and max caps for the visualisation
    vmin = 1000;
    vmax = -1000;
    for(var i = 0; i < proj_xy.length; i++) {
      var mata = proj_xy[i];
      for(var j = 0; j < mata.length; j++) {
          vmax = Math.max(vmax,mata[j]);
          vmin = Math.min(vmin,mata[j]);
      }
    }
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
      colorscale: cs_proj, 
      showscale: false,      
      z: proj_xy, 
      x: x_ax,
      y:y_ax,
      type: "heatmap",
      hovertemplate:'......%{z:.4f}',
      zmin:vmin,
      zmax:vmax,
      name:""
    };

    var trace_atoms = {
      x: atoms_x,
      y: atoms_y,
      mode: 'markers',
      hoverinfo:'skip',
      hovertemplate:'',
      marker: {
          colorscale: cs_atoms,
          color: atoms_v,
          size: 5,
          showscale: false,
          cmin:vmin,
          cmax:vmax,
      },      
    };

    var data = []
    if (proj == "Y" && atoms == "Y"){
      var data = [trace_slice,trace_atoms];
    } else if (proj == "Y"){
      var data = [trace_slice];
    } else if (atoms == "Y"){
      var data = [trace_atoms];
    };
                                  
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
    Plotly.newPlot(div_id, data,layout,config);    
  
  }catch(err){
    alert("make_proj:" + err.message);
  }
}


