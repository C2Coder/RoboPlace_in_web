colors = [
  "#FFFFFF",
  "#E4E4E4",
  "#888888",
  "#222222",
  "#FFA7D1",
  "#E50000",
  "#E59500",
  "#A06A42",
  "#E5D900",
  "#94E044",
  "#02BE01",
  "#00D3DD",
  "#0083C7",
  "#0000EA",
  "#CF6EE4",
  "#820080",
];

chars = [
  "a",
  "b",
  "c",
  "d",
  "e",
  "f",
  "g",
  "h",
  "i",
  "j",
  "k",
  "l",
  "m",
  "n",
  "o",
  "p",
];

server_ip = 'http://hotncold.ddns.net:8080'

function start() {
  display_div = document.createElement("div");
  display_div.id = "display";
  document.body.appendChild(display_div);

  button = document.getElementById("start_button");
  button.remove();

  display_div = document.getElementById("display");

  for (let id = 0; id < 10000; id++) {
    new_div = document.createElement("div");
    //rand_color = Math.floor(Math.random() * 16777215).toString(16);
    //color_string = "#" + rand_color;
    //new_div.style.backgroundColor = color_string;
    new_div.className = "pixel";
    new_div.id = id;
    display_div.appendChild(new_div);
  }

  picture = document.createElement('img');
  picture.src = "static/colors.png"
  document.body.appendChild(picture)
  update();
}

async function fetch_data(section) {
  const url =
    server_ip+"/get_pixels?section=" + String(section);
  const response = await fetch(url);
  fetched_data = await response.text();
  return fetched_data;
}

raw_pixels = "";
function update() {
  raw_pixels = "";
  setTimeout(function() {
    fetch_data(0).then((result) => {
      // Process the result here
      raw_pixels = raw_pixels + result;
    });
  }, 100);
  setTimeout(function() {
    fetch_data(1).then((result) => {
      // Process the result here
      raw_pixels = raw_pixels + result;
    });
  }, 200);
  setTimeout(function() {
    fetch_data(2).then((result) => {
      // Process the result here
      raw_pixels = raw_pixels + result;
    });
  }, 300);
  setTimeout(function() {
    fetch_data(3).then((result) => {
      // Process the result here
      raw_pixels = raw_pixels + result;
    });
  }, 400);
  setTimeout(function() {
    fetch_data(4).then((result) => {
      // Process the result here
      raw_pixels = raw_pixels + result;
    });
  }, 500);
  
  setTimeout(function() {
    //console.log(raw_pixels);
    //raw_pixels = raw_pixels.replaceAll('\n')
    pixels = document.getElementsByClassName('pixel');
    for (let index = 0; index < 10000; index++) {
      pixels[index].style.backgroundColor = colors[chars.indexOf(raw_pixels[index])]
      
    }
    raw_pixels = ""
  }, 1000);
  setTimeout(update, 5000);
}

