$(".bronze").mouseup(function(e){
    if (e.which === 1) {
        var counter = parseInt($(this).next(".bronze_counter").text(), 10)
        console.log(counter)
        if (counter < 3) {
            counter += 1
            $(this).next(".bronze_counter").text(counter);
        }
    }
    else if (e.which === 3) {
        var counter = parseInt($(this).next(".bronze_counter").text(), 10)
        console.log(counter)
        if (counter > 0) {
            counter -= 1
            $(this).next(".bronze_counter").text(counter);
        }
    }

});


$(".silver_gold").mouseup(function(e){
    if (e.which === 1) {
        var counter = parseInt($(this).next(".silver_gold_counter").text(), 10)
        console.log(counter)
        if (counter == 0) {
            counter += 1
            $(this).next(".silver_gold_counter").text(counter);
        }
    }
    else if (e.which === 3) {
        var counter = parseInt($(this).next(".silver_gold_counter").text(), 10)
        console.log(counter)
        if (counter == 1) {
            counter -= 1
            $(this).next(".silver_gold_counter").text(counter);
        }
    }

});


$(".leader").mouseup(function(e){
    if (e.which === 1) {
        var counter = parseInt($(this).next(".leader_counter").text(), 10)
        console.log(counter)
        if (counter == 0) {
            counter += 1
            $(this).next(".leader_counter").text(counter);
        }
    }
    else if (e.which === 3) {
        var counter = parseInt($(this).next(".leader_counter").text(), 10)
        console.log(counter)
        if (counter == 1) {
            counter -= 1
            $(this).next(".leader_counter").text(counter);
        }
    }

});

