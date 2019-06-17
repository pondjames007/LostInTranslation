let count = 0
let round = 3
// let progress = document.querySelectorAll('.progress__step')
// let progress_counter = 0

function enter_event(count){
    let c = count;
    c++
    let description = document.getElementById('userword').value
    document.getElementById('userword').value = ''
    $.post("/", {'description': description}, (resp)=>{
        if(c < round){
            document.getElementById('main_image').src = resp
            
        }
        else{ // finish describing
            $( "#trans_story" ).show();
            $( ".describe" ).slideUp( "slow", function() {
                // Animation complete.
            });
            
            // $([document.documentElement, document.body]).animate({
            //     scrollTop: 180
            // }, 800);

            // progress[0].classList.remove('progress__step--active')
            // progress[1].classList.add('progress__step--active')

            $.post("/", {'story': true}, (resp)=>{
                let images = resp['images']
                let sketches = resp['sketches']
                let descriptions = resp['descriptions']
                let obj_drawn = resp['obj_drawn']
                console.log(images)
                console.log(sketches)
                console.log(descriptions)
                document.getElementById('source_img').src = images[0]
                document.getElementById('sketch_img').src = "data:image/svg+xml;charset=utf-8," + sketches[0]
                document.getElementById('next_img').src = images[1]
                document.getElementById('input_txt').innerText = descriptions[0]
                // document.getElementById('categories_txt').innerText = obj_drawn[0]
                // show story
                let storyCount = 0
                document.getElementById('next').addEventListener('click', ()=>{
                    storyCount++
                    console.log(storyCount)
                    console.log('round: '+ round)
                    if(storyCount == round-1){
                        console.log('ready for rating')
                        document.getElementById('next').innerHTML = "Go Rating"
                    }
                    else if(storyCount > round-1){
                        console.log("here: "+storyCount)
                        // window.location.reload(true)
                        // $( ".rating" ).css('display', 'inline-block');
                        $(".rating").show()
                        $( "#trans_story" ).slideUp( "slow", function() {
                            // Animation complete.
                        });
                        
                        // $([document.documentElement, document.body]).animate({
                        //     scrollTop: 280
                        // }, 800);

                        document.getElementById('refresh').addEventListener('click', ()=>{
                            window.location.reload(true)
                        })
                    }
                    

                    if(storyCount < round){
                        $('#prev').show()
                        document.getElementById('source_img').src = images[storyCount]
                        document.getElementById('sketch_img').src = "data:image/svg+xml;charset=utf-8," + sketches[storyCount]
                        document.getElementById('next_img').src = images[storyCount+1]
                        document.getElementById('input_txt').innerText = descriptions[storyCount]
                        // document.getElementById('categories_txt').innerText = obj_drawn[storyCount]
                    }
                    
                    
                    
                })
                
                document.getElementById('prev').addEventListener('click', ()=>{
                    storyCount--
                    console.log(storyCount)
                    if(storyCount == 0){
                        $('#prev').hide()
                    }
                    
                    document.getElementById('next').innerHTML = "Next Round"
                    
                        
                    document.getElementById('source_img').src = images[storyCount]
                    document.getElementById('sketch_img').src = "data:image/svg+xml;charset=utf-8," + sketches[storyCount]
                    document.getElementById('next_img').src = images[storyCount+1]
                    document.getElementById('input_txt').innerText = descriptions[storyCount]
                    // document.getElementById('categories_txt').innerText = obj_drawn[storyCount]
                    
                })





            })
        }
    })
    return c
}



$.get("/", ()=>{
    console.log('get')
    $.post("/", {'loadnlp': true}, ()=>{
        console.log('nlp loaded')

        document.getElementById('enter').addEventListener('click', (e)=>{
            count = enter_event(count)  
            console.log(count)              
        })
        
        document.getElementById('userword').addEventListener('keypress', (e)=>{
            if(e.which == 13 || e.keyCode == 13){
                count = enter_event(count)
                console.log(count)
            }
            
        })
        
    })
})


document.getElementById('start').addEventListener('click', ()=>{
    $('.wrapper-describe').show();
    $( ".wrapper-intro" ).slideUp( "slow", function() {
        // Animation complete.
    });
    // $( "#step_indicator").show();
    // $( "#q_image" ).show();
    // $( "#answer" ).show();
    
    // $([document.documentElement, document.body]).animate({
    //     scrollTop: 180
    // }, 800);
    
    
    $.post( "/", (resp)=>{
        document.getElementById('main_image').src = resp
    });
})

