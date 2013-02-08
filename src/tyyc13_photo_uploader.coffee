loadPhotos = ->
  $.get '/tyyc13/photo/json', (res) ->
    for photo in res
      $('#grid').append("<div class='grid_item' style='background-image: url(#{photo});')>")
    
    $('.grid_item').click ->
      $('#display').css('background-image', $(this).css('background-image'))
    $('.grid_item:first-child').click()

$ ->
  loadPhotos()
  