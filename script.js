let base64Image;

// IMAGE SELECTOR FUNCTION
$("#image-selector").change(function(){
    let reader = new FileReader();
    reader.onload = function(e){
        let dataURL = reader.result;
        $("#selected-image").attr("src", dataURL);
        base64Image = dataURL.replace("data:image/png;base64,","");
        console.log(base64Image);
    }
    reader.readAsDataURL($("#image-selector")[0].files[0]);

    // ANABLE THE PREDICT BUTTON
    $("#predict-button").removeClass("disabled");
});

// IMAGE PREDICTION FUNCTION
$("#predict-button").click(function(){

    // DISPLAY THE LOADER
    $(".loader").removeClass("hide");
    // DISABLE THE PREDICT BUTTON
    $("#predict-button").addClass("disabled");

    let message = {
        image: base64Image
    }
    console.log(message);
    $.post("http://127.0.0.1:5000/predict", JSON.stringify(message), function(response){

        // SET THE RESULTS AFTER PREDICTION

        // IMAGES
        for(let i=0; i < response.prediction.length; i++ ){
            $("#images-result").after(`<img class="img-result" src=${response.prediction[i]} />`)
        }
        

        $("#name-pred").append(`  >>> This is an image of : <span class="pred-result">${response.name}</span>`);
        $("#accuracy-pred").append(`  >>> With accuracy of : <span class="pred-result">${Math.ceil( response.accuracy * 100 )} %</span>`);

        // HIDE THE LOADER
        $(".loader").addClass("hide");
        console.log(response);
    });
});