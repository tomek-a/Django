// Adding and removing bronze cards from collection to the deck
$(document).on('mouseup', '.card', function(){
    var counter = parseInt($(this).find(".counter").text(), 10);
    var bronze_counter = parseInt($(".bronze_counter").text(), 10)
    var silver_counter = parseInt($(".silver_counter").text(), 10)
    var gold_counter = parseInt($(".gold_counter").text(), 10)
    var leader_counter = parseInt($(".leader_counter").text(), 10)
    console.log(counter)
    var card_class = $(this).attr("class");
    console.log(card_class)
    var card_name = $(this).attr("class").replace(/(card )*(bronze )*(silver )*(gold )*(leader )*/, "");
    console.log(card_name)
    var in_deck = $(this).data("in_deck");
    console.log(in_deck)

    // bronze card add condition
    if (in_deck == "No" && card_class.includes("bronze")){
        if (counter < 3) {
            counter += 1;
            bronze_counter += 1;
            $(this).find(".counter").text(counter);
            $(".deck .bronze_counter").text(bronze_counter)
            if (counter == 1){
                $(this).clone().attr("data-in_deck", "Yes").appendTo(".deck .bronzies");
            }
            else {
                $(".deck ." + card_name).find(".counter").text(counter);
            }

        }
    }
    // silver card add condition
    else if (in_deck == "No" && card_class.includes("silver")){
        if (counter < 1) {
            counter += 1
            silver_counter += 1;
            $(this).find(".counter").text(counter);
            $(".deck .silver_counter").text(silver_counter)
            if (counter == 1){
                $(this).clone().attr("data-in_deck", "Yes").appendTo(".deck .silvers");
            }
            else {
                $(".deck ." + card_name).find(".counter").text(counter);
            }

        }
    }
    // same for gold cards
    else if (in_deck == "No" && card_class.includes("gold")){
        if (counter < 1) {
            counter += 1
            gold_counter += 1;
            $(this).find(".counter").text(counter);
            $(".deck .gold_counter").text(gold_counter);
            if (counter == 1){
                $(this).clone().attr("data-in_deck", "Yes").appendTo(".deck .goldies");
            }
            else {
                $(".deck ." + card_name).find(".counter").text(counter);
            }

        }
    }
    // same for leader cards
    else if (in_deck == "No" && card_class.includes("leader")){
        if (counter < 1) {
            counter += 1
            leader_counter += 1
            $(this).find(".counter").text(counter);
            $(".deck .leader_counter").text(leader_counter);
            if (counter == 1){
                $(this).clone().attr("data-in_deck", "Yes").appendTo(".deck .leaders");
            }
            else {
                $(".deck ." + card_name).find(".counter").text(counter);
            }

        }
    }
    // removing cards from deck condition
    else {
        if (counter > 0) {
            counter -= 1;
            if (counter == 0){
                $(this).remove();
            }
            else {
                $(this).find(".counter").text(counter);
            }
            $(".collection ." + card_name).find(".counter").text(counter);
            if (card_class.includes("bronze")){
                bronze_counter -= 1;
                $(".bronze_counter").text(bronze_counter);
            }
            else if (card_class.includes("silver")){
                silver_counter -= 1;
                $(".silver_counter").text(silver_counter);
            }
            else if (card_class.includes("gold")){
                gold_counter -= 1;
                $(".gold_counter").text(gold_counter);
            }
            else if (card_class.includes("leader")){
                leader_counter -= 1;
                $(".leader_counter").text(leader_counter);
            }


        }
    }

});


