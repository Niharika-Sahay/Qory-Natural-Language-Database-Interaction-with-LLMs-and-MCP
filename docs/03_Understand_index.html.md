The `index.html` file consists of not only HTML elements but also their styling according to **CSS** under the `<style>` tag. It also consists of **JavaScript** under `<script>` tags to handle some logic of how the elements are displayed as well as how data is communicated between various applications of Flask and MongoDB.

I'll be breaking this documentation into **three** main sections - **Understanding JavaScript**, **Understanding HTML** & **Understanding CSS**.\
Let's dig in!

## Understanding JavaScript

Starting with JavaScript may seem counter-intutive as it's the last part of `index.html` but as it covers the frontend logic, I'll be explaining that first.

```
document.getElementById("queryForm").addEventListener("submit", async function (e) {
```
- `document` refers to the entire HTML page.
- `.getElementById("queryForm")` selects the HTML element that has the `id="queryForm"` which is ```<form id="queryForm">``` aka our entire **Search Bar along with the Search Button**.
- `.addEventListener("submit", ... )` attaches a listener to the form. Which means: “When this form is submitted, run this function”. The event type is `"submit"` because it is a `<form>` element.
- `async function (e)` defines the function that runs when the form is submitted.
  `e` stands for **event object**. You can think of it as `i` in `for (int i=0; i<n; i++)` used in looping statements. You can rename it and use any other **valid** variable (like 'y').\
  Why `async`? Because it allows to pause the execution by using `await` and wait for server responses.

```
e.preventDefault();
```
Normally, when a form is submitted:
- The browser refreshes the page.
- It sends the form data traditionally.
- The page reloads.
`preventDefault()` stops that behavior.\
In our case it is essential to stop reloading the page because we are dynamically adding the results of the AI. That means if the page reloads before JavaScript could display it, then it would seem like nothing is happening. Even though everything works perfectly fine but just doesn't get displayed. Logically, you could think of it as:
```
a=1
b=2
c=a+b
```
Even though perfectly calculated and results stored, it didn't display it because you didn't write the print statement.

```
let query = document.getElementById("queryInput").value;
```
- `getElementById("queryInput")` selects the HTML element with `id="queryInput"`, i.e, `<input id="queryInput">` in our code.
- `.value` gets whatever the user typed into that input box.
- `let query` = stores that value in a variable called `query`.
Ex: If user typed: `Action movies above rating 7`, `query` will hold that exact string.

```
let response = await fetch("/query", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: "query=" + encodeURIComponent(query)
});
```
- `fetch("/query", {...})`:
     - `fetch()` sends a request to the server.
     - `"/query"` refers to your Flask route: `@app.route("/query", methods=["POST"])`.
       So this line sends data to your Flask backend.
- `await` tells JavaScript: “Wait until the server responds before moving to the next line.” Without `await`, the code would continue before the server sends data.
- `method: "POST"`: Tells the Server: We are sending data. Not just retrieving data. Your Flask route expects `POST`.
- `headers: { "Content-Type": "application/x-www-form-urlencoded" }`: This tells the server:“The data I'm sending is form-style encoded data.”
- `body: "query=" + encodeURIComponent(query)` sends the actual data.
    - "query=" → name of the parameter
    - encodeURIComponent(query) → safely encodes the user input
      Ex: If the user types: _Action & Comedy_, The `&` could break the request. Encoding converts it into safe format for URL transmission. So the final sent data looks like: `query=Action%20movies%20above%207`.

```
let data = await response.json();
```
- The server responds with JSON.
- This converts the response into a JavaScript object/array.
- `await` waits for that conversion.
In our case, Flask returns: `return jsonify(movie_titles)` \(In the app.py\). So `data` becomes: `["Avatar", "The Dark Knight", "Inception"]` OR `{ error: "Model returned invalid JSON" }`

```
let resultsDiv = document.getElementById("results");
```
This selects HTML element that has `id="results"`, i.e, `<div id="results"></div>` in our case. This is where our movie results will appear.

```
resultsDiv.innerHTML = "";
```
This clears previous results.\
Why? If you don’t clear it: New results would keep stacking below old ones. This resets the display before adding new movies.

```
if (data.error) {
    resultsDiv.innerHTML = "<p style='color:red'>" + data.error + "</p>";
    return;
}
```
If the backend returned: `{ error: "Model returned invalid JSON" }` Then: `data.error` exists. So this block runs. It:
- Displays the error message in red.
- Stops further execution using return.
Without return, the code would continue and crash.

```
if (data.length === 0) {
    resultsDiv.innerHTML = "<p>No movies found.</p>";
    return;
}
```
This handles empty results. If the array has zero movies: `[]`, Then: It displays “No movies found" and Stops the execution.

```
data.forEach(title => {
    resultsDiv.innerHTML += `<div class="movie">${title}</div>`;
});
```
`data` is an array of movie titles as we have seen earlier, `forEach(title => {...})` Loops through each movie title. And it adds this to the HTML:
`<div class="movie">Avatar</div>`, then this: `<div class="movie">Inception</div>`, and so on. That means, it appends movie titles as `div` elements.

## Understanding HTML
This is the simplest and also the shortest code in the entire project. Let's understand it line by line.

```
<div class="img"><img width="80px" src="{{ url_for('static', filename='assets/qory.png') }}" alt="Qory"></div>
```
This displays the image of _Qory_ on the top of the page. 

```
<h2>Hi, I'm Qory.</h2>
<p>What's today's vibe?</p>
```
These are the subsequent h2 headings and paragraph to introduce _Qory_.

```
<div class="search-wrapper">
        <form id="queryForm">
            <div class="input-container">
                <div class="input-wrapper"><input type="text" id="queryInput" placeholder="Action movies above rating 7"
                        autocomplete="off" required></div>
                <button type="submit">Search</button>
            </div>

        </form>
        <div id="results" class="results"></div>
</div>
```
- `search-wrapper`: contains the entire search bar, search button and the results that are going to be displayed after fetch.
- `queryForm`: is the _id_ of the `form` element.
- `input-container`: contains the search bar and search button.
- `input-wrapper`: contains the `input` element.
- `results`: is the `div` that contains all the `movie` that will be fetched and rendered as `div`.

This is how the website looks without any styling:
![Screenshot of the webpage with no styling in CSS](/docs/assets/plain_html.png)

Here you can see that I have purposefully taken highly contrasting colors to show you the container structures.
![Screenshot of the webpage with backgound colors to understand container structuring](/docs/assets/overlapping_colors.png)
- `yellow`: Is the `img` class `div`.
- `dark blue`: Is the actual image of _Qory_.
- `orange`: Is the `h2` heading that says _Hi, I'm Qory_.
- `green`: Is the `p` paragraph that says _What's today's vibe?_
- `beige`: Is the `search-wrapper`.
- `dusty pink`: Is the `queryForm`.
- `red`: Is the `input-container`.
- `bright pink`: Is the `input-wrapper`.
- `gray`: Is the `input` element where the user actually types their search.
- `light blue`: Is the `search-button`.

As you can observe, the `search-wrapper`, `query-form` and `input-container` all cover the same area. And to display the colors, I had to change the width of those containers. This is done for alignment purposes and could be explained through CSS.
![Screenshot of webpage with containers resized and having background colors to better understand html stucturing](/docs/assets/no_overlap.png)

## Understanding CSS

Now, CSS is something that is pretty visual. So, I'll try to include as many pictures to explain as possible.

```
* {
   margin: 0;
   padding: 0;
   box-sizing: border-box;
}
```
This removes default margins and paddings added by the browser. `box-sizing: border-box` is a CSS property value that includes an element's padding and border within its specified width and height, preventing unexpected size increases.

```
body {
            background-color: #AAC4F5;
            color: white;
            font-family: Arial;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
```
Here, body is made to be a flex box so that everthing is centered.

```
h2{
   margin: 5px 0;
   font-size: 50px;
}
```
Margins are applied **outside** the container. So, this actually acts as a way to add gaps between elements. Here, between the `h2` and `p`. The font-size is increased to make the `h2` appear bigger on the screen as there is many elements on the page.

```
p {
     margin: 5px 0 10px 0;
     font-size: 20px;
}
```
Here, the margin property syntax is `margin: top right bottom left` which goes clockwise. Adds a `5px` margin between `h2` and `p` now totaling to a `10px` margin including margin from `h2` as well. And `10px` margin between `p` and the `search-wrapper`. Again the font-size is increased for better visibility.

```
.search-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
```
This is done to make the entire search-wrapper appear centered. This includes the `result` container as well meaning that the movies rendered dynamically should also be centered. That is why `search-wrapper` was introduced in the HTML. If the `search-wrapper` is does not wrap the `result`, the movie names would have been rendered to appear to the left as default, if not styled any other way.

```
input {
    padding: 10px;
    width: 400px;
    font-size: 16px;
    border-radius: 12px;
    border: none;
}
```
`padding` is applied to the inside of the container. This increases the size \(vertical\) of the search bar. `Width` increases the length \(horizontal\) of the search bar. `border-radius` round the corners of the search bar. `border:none` removes the default black border that appears on the search bar.

As you can see, this is the current styling of the webpage.
![Screenshot of webpage with current styles described](/docs/assets/search_improve.png)

```
input:focus {
   outline: none;
}
```
The black border that you can see within the search bar is called **focus outline** and making it `none` removes that.

```
.input-wrapper {
   padding: 4px;
   background: linear-gradient(167deg, #9195F6, #F9F07A);
   border-radius: 12px;
}
```
`input-wrapper` essentially is a box behind the actual `input` element. This is done so that we can apply a gradient-border like look to the search bar as you have seen. Because, there is no CSS property that allows you to apply a gradient-border as it is.

```
.input-container {
   display: flex;
   justify-content: center;
   align-items: center;
   gap: 10px;
}
```
Now, as you had seen in the earlier that while styling, the search button had aligned itself below the search bar. To display it in the same line, we needed to wrap both these elements together in one container that we could turn into a _flexbox_ essentially to solve this problem. Thus, the `input-container` was added to wrap both the `input` element and search button into one container.
![Screenshot of button styled to be in the same line as the search bar](/docs/assets/search_button.png)

```
button {
  padding: 9px;
  font-size: 16px;
  cursor: pointer;
  background: #8CA9FF;
  color: white;
  border: 2px solid black;
}
```
Here, we style the search button. 

```
.results {
   width: 80%;
   transform: translateX(-40px);
   margin: 2px 0;
}
```
Here, we are setting the `width` \(horizontal\) to match the width of the search bar. It has then been translated along the X axis, i.e, moved horizontally to align below the search bar and not the search button. `margin` has been applied to top and bottom so that it creates a gap between the search bar and itself, as well as the body and itself at the bottom.
![Screenshot of webpage after results that are not styled](/docs/assets/results_nostyling.png)

```
.movie {
   padding: 10px 10px;
   border-bottom: 1px solid #333;
   border-radius: 5px;
   margin-bottom: 3px;
}
```
The individual movie titles are rendered inside another `div` element with a class of `.movie`. So, to make then appear more individualistic and spaced, we style their respective container by targeting them with their class `.movie`.

```
.movie:nth-child(even) {
   background: #F5EEE6;
   color: black;
}

.movie:nth-child(odd) {
   background: #f3ebd3;
   color: black;
}
```
Lastly, to make alternative movies apear with a two alternative different background colors, we use the `nth-child()` property of CSS. This makes every **even** numbered movie in the dropdown appear with `#F5EEE6` background color and every **odd** numbered movie in the dropdown appear with `#f3ebd3` background color.
![Screenshot of the final webpage with everything styled and working](/docs/assets/qory_search_results.png)

With this, you are set for success!👑\
Need help with your prompts?\
[Prompt Guide](04_Prompt_Guide.md)




 
