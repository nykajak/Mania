function getVids(){
    /*
    Code that returns all the playlist video DOM elements in a particular playlist.
    */
    let element = document.querySelector("ytd-item-section-renderer.style-scope.ytd-section-list-renderer");
    element = element.querySelector("div#contents");
    element = element.querySelector("div#contents");

    let videos = element.getElementsByTagName("ytd-playlist-video-renderer");
    return videos;
}

async function addOneToQueue(){
    /*
    Code that finds and clicks the add to queue option if the relevant popup is active.
    */
    let element = document.querySelector("ytd-menu-popup-renderer>#items");
    element = document.getElementsByTagName("ytd-menu-service-item-renderer");
    
    await element[0].click();
}

async function addSpecificToQueue(videos,specific){
    /*
    Adds videos from index start to index start + number from videos to queue. High end not included.
    */

    for (let video of videos){
        let url = video.querySelector("div a").href;
        url = url.slice(32,43)

        if (specific.has(url)){
            let button = video.querySelector("div#menu yt-icon-button"); // Finds the button for dropdown.
            await button.click(); // Clicks the more options button and produces dropdown.
            await addOneToQueue(); // Adds the video to the queue.
            index = index + 1;
        }
    }
}

let videos = getVids(); // Gets DOM elements. 
// Put relevant ids here for selection.
let specific = new Set([])
addSpecificToQueue(videos,specific);