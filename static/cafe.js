"use strict";

// UI for showing a button with the current status of whether the logged-inb users likes/unlikes a page

//when user clicks this button, is should use AJAX to change the like/unlike status, and then change the button without refreshing the page

$(".like").on('click', like);
$(".unlike").on('click', unlike);

async function like(evt){
  evt.preventDefault();

  let $cafe = $(evt.target).closest("div");
  let cafe_id = $cafe.attr("data-cafe-id");

  console.log(cafe_id)

  const response = await fetch(`/api/like`, {
    method: "POST",
    body: JSON.stringify({cafe_id}),
    headers: {
    "content-type": "application/json"
    }
  });

  const cafeData = await response.json();
  console.log(cafeData)

}

async function unlike(evt){
  evt.preventDefault();

  let $cafe = $(evt.target).closest("div");
  let cafe_id = $cafe.attr("data-cafe-id");

  const response = await fetch(`/api/unlike`, {
    method: "POST",
    body: JSON.stringify({cafe_id}),
    headers: {
    "content-type": "application/json"
    }
  });

  const cafeData = await response.json();
  console.log("cafedata=", cafeData)
}
