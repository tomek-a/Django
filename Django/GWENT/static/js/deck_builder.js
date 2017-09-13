// Adding and removing bronze cards from collection to the deck
$(document).on('mouseup', '.card', function(){
    var counter = parseInt($(this).find(".counter").text(), 10);
    console.log(counter)
    var card_name = $(this).attr("class").replace(/(card )*(bronze )*(silver_gold )*(leader )*/, "");
    console.log(card_name)
    var in_deck = $(this).data("in_deck");
    console.log(in_deck)
    if (in_deck == "No"){
        if (counter < 3) {
            counter += 1
            $(this).find(".counter").text(counter);
            if (counter == 1){
                $(this).clone().attr("data-in_deck", "Yes").appendTo(".deck");
            }
            else {
                $(".deck ." + card_name).find(".counter").text(counter);
            }

        }
    }
    else {
        if (counter > 0) {
            counter -= 1
            if (counter == 0){
                $(this).remove()
            }
            else {
                $(this).find(".counter").text(counter);
            }
            $(".collection ." + card_name).find(".counter").text(counter);
        }
    }

});


