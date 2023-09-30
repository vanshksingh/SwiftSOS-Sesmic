st_css="""
  <style>
  /*Main app page*/
  /* main page
  .css-ffhzg2 {
    background: rgb(14, 17, 23);
  }*/
  .css-k1ih3n{
    padding-top: 0 !important;
    top: -20px !important;
  }
  .css-1avcm0n.e8zbici2 {
    height:0 !important;
    background: none;
  }
  .css-14xtw13.e8zbici0 .css-1rs6os.edgvbvh3 {
    margin-right: 20px !important;
  }
  .css-k1ih3n{
    padding: 1.8rem 3.5rem 1rem !important;
  }

  
  </style>
"""

map_css = """
{% macro html(this, kwargs) %}
    <head>
       
    </head>
    
    <style>
/* Marker PopUp Box CSS */
        .leaflet-popup-content-wrapper{
            padding: 1px;
            text-align: left;
            border: 4px solid #d7a45d;
            border-radius: 12px;
            /*GLASSMORPHISM EFFECT*/
            background: rgba( 28, 25, 56, 0.25 );
            box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
            backdrop-filter: blur( 4px );
            -webkit-backdrop-filter: blur( 4px );
            border: 4px solid rgba( 215, 164, 93, 0.2 );
        }
        .leaflet-popup-content{
            margin: 13px 24px 13px 20px;
            font-size: 1.2em;
            line-height: 1.3;
            min-height: 1px;
        }
        .popinfo {
            width: max-content;
            border-radius: 5px;
            color: #993200;
        }
        .popinfo h5{
            text-align: center;
        }
        .popinfo span{
            font-weight: bold;
            color: #9d3a00;
        }
        .popinfo b{
            font-weight: 800;
            font-family: bariol;
            font-size: 1.4em;
        }
        .leaflet-popup-tip{
            background: #d7a45d !important;
        }

/* Layer Control Panel CSS */

        .leaflet-control-layers-list {
            width: 14vw;
            min-width: 130px;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .leaflet-control-layers form {
            z-index: 10000;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .leaflet-control-layers-group-label{
            padding: 2px;
            margin: 2px;
            background-color: #d75d5d;
            border: 1px dashed black;
            border-radius: 4px;
            text-align: center;
        }
    </style>

{% endmacro %}
"""
