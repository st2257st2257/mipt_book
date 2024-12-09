<template>
  <div>
    <button >Show Popup</button>
  </div>

<svg
    width="1300"
    height="1300"
    id="mySvg"
    style="background-image: url(https://www.baryon.ru/wp-content/uploads/2021/02/%D1%81%D0%B5%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9.png); background-size: contain;"></svg>
<div id="coordinates">

</div>


<form>
<div id="my_data" style="padding-bottom: 100px;">
    <button>Отправить</button>
    <div>
        <input value="id"/>
        <input value="x"/>
        <input value="y"/>
        <input value="width"/>
        <input value="height"/>
    </div>
</div>
</form>



</template>


<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue';

interface ClickData {
    x: number;
    y: number;
}

interface RectData {
    id: number;
    x: number;
    y: number;
    w: number;
    h: number;
}

let click_data_array: Ref<RectData[]> = ref([]);

function myDeleteRect(idToRemove: number) {
    console.log("idToRemove: ", idToRemove);
    click_data_array.value = click_data_array.value.filter(rect => rect.id !== idToRemove);
    UpdateAllRect();
}

function UpdateAllRect() {
    const coordinatesDiv = document.getElementById('my_data');
    const rectDiv = document.getElementById('mySvg');
    console.log(coordinatesDiv);
    if (coordinatesDiv != null) {
        while (coordinatesDiv.firstChild) {
            coordinatesDiv.removeChild(coordinatesDiv.lastChild);
        }
        while (rectDiv.firstChild) {
            rectDiv.removeChild(rectDiv.lastChild);
        }
        click_data_array.value.forEach((rect) => {
            addRectangle(
                rect.x,
                rect.y,
                rect.w,
                rect.h,
                "#ecf",
                "#fce",
                rect.id);
            addRoom(
                rect.x,
                rect.y,
                rect.w,
                rect.h,
                rect.id);
        });
    }
}


onMounted(()=>{
    console.log(9999);

      const svg = document.getElementById('mySvg');
      const coordinatesDiv = document.getElementById('coordinates');
      let firstClick: ClickData | null = null;
      var id = 0;


    console.log(svg);
    console.log(coordinatesDiv);
        if ( (svg != null) && (coordinatesDiv != null) ){
            console.log(9888);
            svg.addEventListener('click', (event) => {
              const svgRect = svg.getBoundingClientRect();
              const x = event.clientX - svgRect.left;
              const y = event.clientY - svgRect.top;

              if (!firstClick) {
                  firstClick = { x, y };
                  coordinatesDiv.textContent = `X:${x.toFixed(2)} Y:${y.toFixed(2)}`;
              } else {
                  const secondClick = { x, y };
                  const distanceX = Math.abs(secondClick.x - firstClick.x);
                  const distanceY = Math.abs(secondClick.y - firstClick.y);
                  const distance = Math.sqrt(Math.pow(secondClick.x - firstClick.x, 2) + Math.pow(secondClick.y - firstClick.y, 2));
                  coordinatesDiv.textContent = `X:${firstClick.x.toFixed(2)} Y:${firstClick.y.toFixed(2)}) W:${distanceX.toFixed(2)}\n H:${distanceY.toFixed(2)}`;

                  addRectangle(
                      Number(`${firstClick.x}`),
                      Number(`${firstClick.y}`),
                      Number(distanceX.toFixed(2)) + 1,
                      Number(distanceY.toFixed(2)) + 1,
                      "#ecf",
                      "#fce",
                      id);
                  addRoom(
                      Number(`${firstClick.x}`),
                      Number(`${firstClick.y}`),
                      Number(distanceX.toFixed(2)) + 1,
                      Number(distanceY.toFixed(2)) + 1,
                      id);
                   // Добавляем в локальный массив
                  const point = {
                      id: id,
                      x: Number(`${firstClick.x}`),
                      y: Number(`${firstClick.y}`),
                      w: Number(distanceX.toFixed(2)) + 1,
                      h: Number(distanceY.toFixed(2)) + 1,};
                  click_data_array.value.push(point);
                  console.log(click_data_array.value);

                  firstClick = null;
                  id = id + 1;
              }
          });
      }
});


function addRectangle(
        x: number,
        y: number,
        width: number,
        height: number,
        fillColor: string,
        strokeColor: string,
        id: number) {
    var svgns = "http://www.w3.org/2000/svg";
    var rect = document.createElementNS(svgns, 'rect');
    rect.setAttribute('x', String(x));
    rect.setAttribute('y', String(y));
    rect.setAttribute('height', String(height));
    rect.setAttribute('width', String(width));
    rect.setAttribute('fill', '#F00');
    rect.setAttribute('stroke', 'blue');
    rect.setAttribute('stroke-width', '3');
    rect.setAttribute('stroke-dasharray', 'v');
    rect.setAttribute('rx', '10');
    // stroke:blue; stroke-width:3; stroke-dasharray:5 5; fill:lightgreen;" rx="10" ry="10
    // rect.setAttribute('fill', '#'+Math.round(0xffffff * Math.random()).toString(16));

    let mySvg = document.getElementById('mySvg');
    if (mySvg != null) {
        mySvg.appendChild(rect);
    }
 }

function addRoom(
        x: number,
        y: number,
        width: number,
        height: number,
        id: number) {
    var new_room = document.createElement('div');

    // Добавляем вводимые значения
    var input_id = document.createElement('input');
    input_id.setAttribute('type', 'number');
    input_id.setAttribute('value', String(id));
    var input_x = document.createElement('input');
    input_x.setAttribute('type', 'number');
    input_x.setAttribute('value', String(x));
    var input_y = document.createElement('input');
    input_y.setAttribute('type', 'number');
    input_y.setAttribute('value', String(y));
    var input_w = document.createElement('input');
    input_w.setAttribute('type', 'number');
    input_w.setAttribute('value', String(width));
    var input_h = document.createElement('input');
    input_h.setAttribute('type', 'number');
    input_h.setAttribute('value', String(height));

    // Добавляем кнопки редактирования элементов
    var b_delete = document.createElement('button');
    b_delete.textContent = 'Удалить';
    b_delete.setAttribute('type', "reset");

    b_delete.addEventListener('click', () => {
        myDeleteRect(id);
      });


    // Добавляем элементы в строку
    new_room.appendChild(input_id);
    new_room.appendChild(input_x);
    new_room.appendChild(input_y);
    new_room.appendChild(input_w);
    new_room.appendChild(input_h);
    new_room.appendChild(b_delete);

    let my_data = document.getElementById('my_data');
    if (my_data) {
        my_data.appendChild(new_room);
    }
  }


</script>

<style scoped>

</style>
