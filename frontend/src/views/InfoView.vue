<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose, provide, inject} from 'vue';


interface Audience_status {
  description: string,
  name: number
}

interface Institute {
  description: string,
  name: string
}

interface Audience {
  number: string,
  number_of_users: number,
  description: string,
  building: Building,
  audience_status: Audience_status
}

interface Building {
  name: string,
  number: string,
  institute: Institute,
  description: string
}

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

let audiences: Ref<Audience[]> = ref([]);
let audiences_gk: Ref<Audience[]> = ref([]);
let audiences_lk: Ref<Audience[]> = ref([]);

onMounted(()=>{
  // username.value = localStorage.getItem("username");
  loadAudience();
});

async function loadAudience(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        // token.value = null;
        localStorage.removeItem("auth-token");
      }
    }

    const data_number = await response.json() as Audience[];
    audiences.value = data_number;
    audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    // username.value = data_number[0].username;
    // number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header data_number:', data_number);
    // console.log('Ответ от сервера header username:', username);
    // console.log('Ответ от сервера header number_bb:', number_bb);
    // console.log('Ответ от сервера header username.value:', username.value);
    // console.log('Ответ от сервера header number_bb.value:', number_bb.value);
    // user_name.first_name = data.name.first_name;
    // user_name.last_name = data.name.last_name;
    // user_name.third_name = data.name.third_name;
    // institute_group.value = data.institute_group;
    // book_rating.value = data.book_rate;
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

const filteredItems = () => {
   let items: { id: number, name: string, age: number }[]  = [
        { id: 1, name: 'Иван', age: 25 },
        { id: 2, name: 'Мария', age: 30 },
        { id: 3, name: 'Петр', age: 28 }
      ];

  return items; //.filter(item => item.age > 25);
};

defineExpose({ filteredItems });


</script>

<template>


       <header>
        <h1>Система бронирования аудиторий МФТИ</h1>
        <img src="https://old.mipt.ru/upload/medialibrary/b0c/mipt_rus.png" alt="Логотип МФТИ">
    </header>
    <main>
        <section id="intro">
            <h2>Добро пожаловать!</h2>
            <p>
                Эта страница содержит информацию о системе бронирования аудиторий МФТИ.
                Здесь вы найдете подробное описание системы баллов, правила бронирования,
                а также полезные ссылки и инструкции.
            </p>
        </section>
        <section id="system">
            <h2>Система бронирования</h2>
            <h4>Баллы бронирования (ББ)</h4>
            <p>
                Система бронирования аудиторий МФТИ основана на системе баллов бронирования.
                Количество доступных баллов одинаково
                для всех учащихся и преподавателей. Каждый день пользователю
                начисляется 4 балла бронирования (ББ). Всего у пользователя может
                быть не более 28 ББ. Число баллов бронирования в отсутствии полной
                загруженности соответствует числу пар, которые можно забронировать.
                Это число может меняться.

            </p>
            <h4>Аукцион аудиторий</h4>
            <p>
                При наличии высокой загруженности аудииторий вы можете выставить Число
                ББ саостоятельно или автоматически. В случае выставления ББ самостоятельно
                вы отправляете свою заявку на аукцион, в котором N заявок соревнуются за
                M мест бронирования. В случае автоматического выставления баллов бронирования
                система подбирает наименьшее число ББ, требуемых для наиболее вероятного бронировая
                аудитории. Система автоматических баллов бронирования настроена на 90%
                шанс бронирования аудитории.
            </p>
            <h4>Приоритет семинаров</h4>
            <p>
                Все бронирования деляться на две группы: административные и студенческие.
                Любое административное мероприятие имеет абсолютный приоритет над студенческим.
                Бронирования делатсья на группы по приоритету и выставляются на аукцион от меньшего
                к большему.
                Приоритет выглядит следующим образом:
            </p>
            <table>
                <thead>
                    <tr>
                        <th>№</th>
                        <th>Тип мероприятия</th>
                        <th>Должность</th>
                        <th>ББ за пару</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th>1</th>
                        <td>Плановое занятие по расписанию</td>
                        <td>Администрация</td>
                        <td></td>
                    </tr>
                    <tr>
                        <th>2</th>
                        <td>Заседания научных советов</td>
                        <td>Администрация</td>
                        <td></td>
                    </tr>
                    <tr>
                        <th>3</th>
                        <td>Зачеты и экзамены</td>
                        <td>Администрация</td>
                        <td></td>
                    </tr>
                    <tr>
                        <th>4</th>
                        <td>Конференции</td>
                        <td>Администрация</td>
                        <td></td>
                    </tr>
                    <tr>
                        <th>5</th>
                        <td>Семинары</td>
                        <td>Семинаристы</td>
                        <td>1 шт</td>
                    </tr>
                    <tr>
                        <th>6</th>
                        <td>Консультации</td>
                        <td>Семинаристы</td>
                        <td>1 шт</td>
                    </tr>
                    <tr>
                        <th>7</th>
                        <td>Студенческие бронирования</td>
                        <td>Студенты</td>
                        <td>1 - 28 шт</td>
                    </tr>
                </tbody>
            </table>
            <p>
                Для того, чтобы пользоваель, стал саминаристом, ему нужно отправить
                соответствующее обращение на почту: <a href="info@mipt.site">info@mipt.site</a>
            </p>

            <h4>Совместные бронирования</h4>
            <p>
                В систему бронирования внедрена система предпочтений, которая позволяет
                бронировать аудитории совместно, основываясь на приоритетах пользователя.
                Число ББ, списанных со счёта будет разделено поровну между всеми находящимися
                в аудитории.
            </p>
            <p>
                Список приоритетов включает:
                "Тихая аудитория",
                "Одинаковый курс",
                "Одинаковый факультет",
                "Открытое окно",
                "Тихая музыка",
                "Вкусный чай/кофе",
                "Совместное обсуждение",
                "Выбранная таматика"
            </p>


        </section>
        <section id="rules">
            <h2>Правила бронирования</h2>
            <p>
                Бронирование аудиорий осуществляется по следующим правилам, необходимым
                для комфортного бронирования аудиторий.
            </p>
            <ul>
                <li>Заявка на бронирование подается через онлайн-систему.</li>
                <li>Бронирование возможно только на текущий день.</li>
                <li>Отмена и завешение осществляются через онлайн-систему.</li>
                <li>Бронирование аудитории возможно только в отведенные временные слоты.</li>
                <li>Бронирование аудиторий включает рейтинг добросовестности влияющий на ББ за пару.</li>

            </ul>
            <h4>Рейтинг бронирования</h4>
            Система включает рейтинг бронирования, имеющий значение от 0 до 7.
            Стоимость бронирования аудитории для пользователя выражается как
            <p> ББ = alpha * (7 / рейтинг) </p>
            <p>
                Рейтинг бронирования падает на 20% каждый раз, когда пользователь бронирует
                аудиторию и, не отменив бронирование, ей не пользуется (при бронировании нескольких
                аудиторий 20% списывается за каждую аудиторию). Фиксация нарущения осуществляется
                через приложение.
            </p>
            <p>
                Падает каждый раз на 50%, когда пользовтель бронирует
                несколько аудиторий в отсутствии цели воспользовтя каждой из забронированных.
            </p>
            <p>
                Падает каждый раз на 100%, когда пользовтель намеренно пытается сломать систему бронирования.
            </p>
            <p>
                Пользователь получает получет каждую неделю по 20% рейтинга, но не более 7 единиц.
            </p>
        </section>
        <section id="contact">
            <h2>Контакты</h2>
            <p>
                По вопросам бронирования аудиторий обращайтесь по адресу: <br>
                <a href="info@mipt.site">info@mipt.site</a>
            </p>
        </section>
    </main>

</template>

<style scoped>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

header {
    background-color: #333;
    color: #fff;
    padding: 20px;
    text-align: center;
}

header img {
    max-width: 150px;
    margin: 0 auto;
}

main {
    max-width: 960px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

section {
    margin-bottom: 30px;
}

h2 {
    color: #333;
    margin-top: 0;
}

p {
    line-height: 1.6;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
}

th {
    background-color: #eee;
}

ul {
    list-style: disc;
    margin-left: 20px;
}

footer {
    text-align: center;
    padding: 10px;
    background-color: #333;
    color: #fff;
}

a {
    color: #337ab7;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

</style>
