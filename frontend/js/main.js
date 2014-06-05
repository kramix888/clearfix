var clearfix = {
  front:{
    init: function() {
      var e = this;
        e.Slider();
        e.inserticon();
        e.initialize_foundation();  
    },
    Slider: function() {

      $('.flicker-slider-main').flicker({
        'arrows' : false
      });

      $('.flicker-slider-secondary').flicker();
      
      $('.flicker-slider-tertiary').flicker(); 

    },   
    inserticon: function() {

       $('.flickerplate .arrow-navigation.left .arrow').append("<i class='fa fa-angle-left'></i>");
       $('.flickerplate .arrow-navigation.right .arrow').append("<i class='fa fa-angle-right'></i>");
        
    }        
  


  },
  sub:{
    init: function(){
      this.grabimage();
      this.flowup();
    },
     grabimage: function() {         

        $(".layout-featured img").each(function(i, elem) {
          var img = $(elem);
          var div = $("<div />").css({
            background: "url(" + img.attr("src") + ") no-repeat",
            width: $(".layout-featured").width() + "px",
            height: 388 + "px"
          });

          div.html(img.attr("alt"));
          div.addClass("replacedImage");
            
          img.replaceWith(div);
        });

     },
     flowup: function(){
       $("body").flowUp(".group-item", { transalteY: 350, duration: 1 });
      }
     }
  
}



    

       