from app.db.models import *
from app.utils.utils_of_security import get_password_hash


@db_session
def create_pages():

    SimpleEntity(key="partner", data={
        1: dict(name="Минестерство промышленности, транспорта и иннавационной политики Пензенской области",
                image="img/partners/MinesterstvoPromPO.jpg"),
        2: dict(name="Минестерство образования Пензенской области", image="img/partners/MinesterstvoPromPO.jpg"),
        3: dict(name="ГКУ “Пензенское региональное объеденение бизнес-инкубаторов”",
                image="img/partners/BisnesIncubatorGroup.jpg"),
        4: dict(name="Молодежный отряд “Новатор”", image="img/partners/MO_Novator.jpg")
    })

    SimpleEntity(key="socials", data={
        1: dict(name="facebook", icon="img/socials/f_book.png", link="https://www.facebook.com/1000listnick/"),
        2: dict(name="instagram", icon="img/socials/insta.png", link="https://www.instagram.com/1000listnick/"),
        3: dict(name="youtube", icon="img/socials/youtube.png",
                link="https://www.youtube.com/channel/UC21S9sVTzKc0__CgifzJlow"),
        4: dict(name="Вконтакте", icon="img/socials/Vk.png", link="https://vk.com/official1000listnick"),
    })
    commit()

    main = Page(
        page_url="/",
        page_path="content/templates/main.html",
        visible=True,
        title="Главная"
    )
    event_main = Page(
        page_url="/events",
        page_path="content/templates/events/event_main.html",
        is_header=True,
        title="Список всех событий"
    )
    commit()
    teengrad = Page(
        page_url="/events/teengrad",
        page_path="content/templates/events/teengrad.html",
        visible=True,
        title="TeenГрад",
        root_page=event_main
    )
    dominno = Page(
        page_url="/events/dominno",
        page_path="content/templates/events/dominno.html",
        visible=True,
        title="ДомInno",
        root_page=event_main
    )
    brainstorm = Page(
        page_url="/events/brainstorm",
        page_path="content/templates/events/brainstorm.html",
        visible=True,
        title="brainstorm",
        root_page=event_main
    )
    innovatorium = Page(
        page_url="/events/innovatorium",
        page_path="content/templates/events/innovatorium.html",
        visible=True,
        title="innovatorium",
        root_page=event_main
    )
    season_start = Page(
        page_url="/events/season_start",
        page_path="content/templates/events/season_start.html",
        visible=True,
        title="season_start",
        root_page=event_main
    )
    success_factor = Page(
        page_url="/events/success_factor",
        page_path="content/templates/events/success_factor.html",
        visible=True,
        title="success_factor",
        root_page=event_main
    )
    news_main = Page(
        page_url="/news",
        page_path="content/templates/news/news_main.html",
        visible=True,
        is_header=True,
        title="Новости",
    )
    about_program = Page(
        page_url="/about_program",
        page_path="content/templates/about_program.html",
        visible=True,
        is_header=True,
        title="О нас",
    )
    competition = Page(
        page_url="/competition",
        page_path="content/templates/competition/main_novator_web.html.html",
        visible=True,
        is_header=True,
        title="Новатор веб",
    )
    # news_main = Page(
    #     page_url="/competition",
    #     page_path="content/templates/competition/direction.html",
    #     visible=True,
    #     title="Новатор веб",
    #     root_page=event_main
    # )
    videostudy = Page(
        page_url="/videostudy",
        page_path="content/templates/videostudy/main_videostudy.html.html",
        visible=True,
        title="videostudy",
        is_header=True,
        root_page=event_main
    )

    commit()

    SimpleEntity(key="partner", data={
        1: dict(name="Минестерство промышленности, транспорта и иннавационной политики Пензенской области",
                image="img/partners/MinesterstvoPromPO.jpg"),
        2: dict(name="Минестерство образования Пензенской области", image="img/partners/MinesterstvoPromPO.jpg"),
        3: dict(name="ГКУ “Пензенское региональное объеденение бизнес-инкубаторов”",
                image="img/partners/BisnesIncubatorGroup.jpg"),
        4: dict(name="Молодежный отряд “Новатор”", image="img/partners/MO_Novator.jpg")
    })

    SimpleEntity(key="socials", data={
        1: dict(name="facebook", icon="img/socials/f_book.png", link="https://www.facebook.com/1000listnick/"),
        2: dict(name="instagram", icon="img/socials/insta.png", link="https://www.instagram.com/1000listnick/"),
        3: dict(name="youtube", icon="img/socials/youtube.png",
                link="https://www.youtube.com/channel/UC21S9sVTzKc0__CgifzJlow"),
        4: dict(name="Вконтакте", icon="img/socials/Vk.png", link="https://vk.com/official1000listnick"),
    })

    News(
        page_url="/news/mediaForum",
        page_path="content/templates/news/mediaForum.html",
        visible=True,
        title="1000-list-nick на медиафоруме",
        root_page=news_main,
        image="img/news/mediaForum.jfif",
        description=" 4-7 сентября в Пензе впервые проходит Всероссийский молодежный медиафорум «mediaАКЦЕНТ». Молодых журналистов региональных СМИ, фотографов, видеографов, специалистов сферы SMM, студентов и абитуриентов профильных специальностей ждёт насыщенная программа форума. На форуме была оборудована площадка «1000-list-nick». На площадке любой желающий мог узнать информацию о программе, её направлениях, мероприятиях и проектах",
    )
    News(
        page_url="/news/start_2019",
        page_path="content/templates/news/start_2019.html",
        visible=True,
        title="Старт сезону дан!",
        root_page=news_main,
        image="img/news/start_2019.jfif",
        description="11 октября 2019 года в рамках работы программы «1000-list-nick» стартует комплекс интернет- конкурсов «Новатор_Web». Победители и призеры комплекса получат... "
    )
    News(
        page_url="/news/seminar",
        page_path="content/templates/news/seminar.html",
        visible=True,
        title="Семинар - стажировка",
        root_page=news_main,
        image="img/news/seminar.jfif",
        description="""28-29 сентября состоялся семинар-стажировка "От детского проекта к стартапу"Для участников мероприятия прошел авторский тренинг "Новые ресурсы человека в социуме...""",
    )
    commit()

    Direction(
        name="IT",
        icon="img/directions/it.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_885c36fc8e1d4fdd9c281d58e1901d17/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_65b0e4979a5442f88d6a38f15c606853/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_d8a2689feb914605879819c35d74290b/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_875262dbd5d443e58cb11c9b54be1806/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_086a98241c6845319cf5781f5ddc5825/1080p/mp4/file.mp4"
        }
    )
    Direction(
        name="3D",
        icon="img/directions/3d.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_6bc1b38b9eed42ddab5994e13b37fc95/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_0dd4ec30189944d682fccd258ee758a1/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_583b19a059a149aa9a73f66d7fe7d439/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_9dca029c88474fc1a20ed8a9d06c4ea9/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_3e1e4460d8ee4187a098652fcb6307a4/1080p/mp4/file.mp4",
        }
    )
    Direction(
        name="Engineer",
        icon="img/directions/engineer.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_c45dc14ee30b46c2a8d2a7891580adf5/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_2a592617b02346d7a0c97ca2121d0fdf/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_281e619df1db4ffeb734d4e39be30226/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_e8fbca8b1af340468732d507627c47b3/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_7f57a8ef545a4c3fa30e2c9026a64fed/1080p/mp4/file.mp4"
        }
    )
    Direction(
        name="Design",
        icon="img/directions/design.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_22c6be65403a41398f97904f4d9bd39c/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_e116b6a6f2794bc5b13291bca556f642/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_47059379f4434744bb0c09f702dd3381/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_8d13ea570a8d420ca7bef30221a5b38f/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_5fc5e01f7d224ed193007537938505fd/1080p/mp4/file.mp4"
        }
    )
    Direction(
        name="PM",
        icon="img/directions/pm.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_4890fdcae2b74eebb28091e4a8267870/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_0efb8386339d4ebd8fb92bf6a656b6b6/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_869af7c8e18142abb5482a81bf32759f/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_48505e745ed94027954aec9bf5e2124a/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_78ce211f9bb94e4c8e71a3c09b0753d3/1080p/mp4/file.mp4"
        }
    )
    Direction(
        name="SMM",
        icon="img/directions/smm.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_53b245f42ec14a29bb96204605226fd8/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_573978293eb74120b30c7a3efdbda4d4/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_59e17b3b8398426e8b127df69e116cff/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_11a8bd0fd65b4fc3a570308f9c193460/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_9bb1b8455ce44e34bc5c8c5505fe9cf6/1080p/mp4/file.mp4"
        }
    )
    Direction(
        name="Video",
        icon="img/directions/video.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_3f557878d22645c192182aee325010ac/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_f57c2eef03e84de0920e3114ca38017c/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_2037abccbf9140e9af6dfcfde0411ef9/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_adfb55c613ef4971ae03a4d2ee86edf7/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_834a9ce6af104b94803d624b2ffa4386/1080p/mp4/file.mp4"
        }

    )
    Direction(
        name="Hardware",
        icon="img/directions/hardware.png",
        video_lessons={
            1: "https://video.wixstatic.com/video/9a5d54_aac2f2b6be0348fdb31f2d721fa48846/1080p/mp4/file.mp4",
            2: "https://video.wixstatic.com/video/9a5d54_cdc5f9d5795c417792d68dfc8b3e3ba4/1080p/mp4/file.mp4",
            3: "https://video.wixstatic.com/video/9a5d54_cf94349966d348418832f8cc4486c241/1080p/mp4/file.mp4",
            4: "https://video.wixstatic.com/video/9a5d54_85fff24458b141439c6ab7a95461b856/1080p/mp4/file.mp4",
            5: "https://video.wixstatic.com/video/9a5d54_b8c6230d450949d2be2b6b102b0336d2/1080p/mp4/file.mp4"
        }
    )
    commit()
    qu_ans = {
        "Где проходит Teenград?": """Летняя школа проводится на базе ГАОУ ПО «Училища олимпийского резерва Пензенской области» (г. Пенза, ул. Одоевского, 1). 
                                                        <a class="no-effect" href="https://goo.gl/maps/aLdAoZ4YmSpCDpQT7"> <i class="fas fa-map-marked-alt"></i> </a>""",
        "Как попасть в Teenград?": """<p> Есть два пути:</p>
                                          <p>1) Принимай участие в осеннем этапе интернет-конкурса Novator_Web.
                                             10 победителей в каждом из 8 направлений прокачают свои знания на зимней школе, по 
                                             результатам которой наиболее отличившиеся участники получат путевки в TeenГрад.</p>
                                          <p>2) Участвуй в весеннем этапе интернет-конкурса Novator_Web. 
                                               10 победителей в каждом из 8 направлений получают путевки в летнюю школу.
                                          </p>""",
        "Есть ли возрастные ограничения?": """Ты можешь принять участие в летней школе, если тебе от 14 до 18 лет.""",
        "Участие в летней школе бесплатное?": """Все мероприятия 1000-list-nick абсолютно бесплатные! """,
        "Даёт ли Teenград привелегии при поступлении в ВУЗ?": """По решению молодежного отдела и отряда «Новатор» самые талантливые участники могут получить до 10 баллов к ЕГЭ для поступления в Пензенские ВУЗы.""",
        'Что такое молодежный отряд "Новатор"?': """ Участники молодежного отряда «Новатор» - это студенты ВУЗов, старших курсов ССУЗов или уже окончившие обучение ребята. 
                                                                            Они берут на себя функции тьюторов, руководителей лабароторий и клубов, и делают всё для того, чтобы мероприятия программы были познавательными, 
                                                                            яркими и запоминающимися.
                                                                            Именно эти ребята дарят вам незабываемые впечатления и создают теплую атмосферу 1000-list-nick. """,
        "Что такое МИП?": """МИП - малое инновационное предприятие, или если проще - то команда
                                                 перспективных молодых людей, знатоков своего дела, которые объединились
                                                  для разработки общего проекта."""
    }

    for key, val in qu_ans.items():
        Question(
            question=key,
            answer=val,
            pages=[teengrad],
            was_read=True,
            was_answered=True,
        )
    qu_ans1 = {
        "Где проходит ДомInno?": ''' ГАОУ по училище олимпийского резерва Пензенской области, г. Пенза, улица Пугачёва, 93.
                    <a class="no-effect" href="https://goo.gl/maps/LvsGwqqYVjTaSDnBA"> <i class="fas fa-map-marked-alt"></i>
                    </a>''',
        "Как попасть в ДомInno?": '''Необходимо принять участие в осеннем этапе интернет-конкурса
                      «Новатор_Web», 10 победителей в каждом направлении получают
                      путевки в зимнюю школу.''',
        "Есть ли возрастные ограничения?": ''' Ты можешь принять участие в зимней школе, если тебе от 14 до 18 лет.''',
        "Участие в зимней школе бесплатное": ''' Все мероприятия 1000-list-nick абсолютно бесплатные''',
        "Что если у меня нет опыта участия в подобных конкурсах?": ''' Все когда-то делают первый шаг. Если ты только начинаешь свой путь к профессии мечты, заходи
                      в раздел VideoStudy и изучай видео-уроки от наших специалистов, они помогут тебе справиться с
                      заданием. Мы в тебя вери''',
    }
    for key, val in qu_ans1.items():
        Question(
            question=key,
            answer=val,
            pages=[dominno],
            was_read=True,
            was_answered=True,
        )

    User(
        username="KalekinDaniil",
        hash_password=get_password_hash("KalekinDaniil123"),
        name="Даниил",
        surname="Калекин",
        email="KalekinDaniil123@mail.ru",
        date_of_birth=date(2000, 4, 4),
        about_program="Знания которые дают в программе невозможно получить в школе. Тут каждый хочет чем-то делиться и узнавать в ответ",
        direction="SMM",
        visible_about_program_field=True,
        photo="img/humans/KalekinDaniil.png"

    )
    User(
        username="DmitriyShelahaev",
        hash_password=get_password_hash("DmitriyShelahaev321"),
        name="Дмитрий",
        surname="Шелахаев",
        email="Dmitriy.Shelahaev@mail.ru",
        date_of_birth=date(2000, 2, 4),
        about_program='''Программа "1000-list-nick" - необъятная тема. Дала мне она очень и очень много. В первую очередь - 
                          знакомства с огромным количеством людей, умение работать в команде, кучу положительных эмоций.''',
        direction="Engeneer",
        visible_about_program_field=True,
        photo="img/humans/DmitriyShelahaev.png"

    )
    User(
        username="DmitriyGirkin",
        hash_password=get_password_hash("DmitriyGirkin42"),
        name="Дмитрий",
        surname="Жиркин",
        email="Dmitriy.Girkin@mail.ru",
        date_of_birth=date(2000, 2, 4),
        about_program="1000-list-nick дал развитие моим способностям, дал мне возможность найти дело по душе, подарил мне много друзей и знакомых,",
        direction="IT",
        visible_about_program_field=True,
        photo="img/humans/DmitriyGirkin.png"

    )


