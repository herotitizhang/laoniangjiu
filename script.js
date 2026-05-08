const characters = {
  mao_mengda: {
    name: "毛猛达",
    text: "侬勿要急，事体总归要一桩桩讲清爽。饭要趁热吃，道理也要趁热讲。",
    avatar: "assets/portraits/mao_mengda/Screenshot%202026-05-07%20204353.png",
  },
  chen_guoqing: {
    name: "陈国庆",
    text: "大家坐下来慢慢讲。人情归人情，规矩归规矩，弄堂里的事最怕一句气话伤了和气。",
    avatar: "assets/portraits/chen_guoqing/Screenshot%202026-05-07%20204143.png",
  },
  yao_qier: {
    name: "姚祺儿",
    text: "哎呀，这点小事体也要板面孔啊？笑一笑嘛，办法总比烦恼多一点。",
    avatar: "assets/portraits/yao_qier/Screenshot%202026-05-07%20203928.png",
  },
  li_jiusong: {
    name: "李九松",
    text: "我就是想问个清楚呀。讲道理嘛，讲到最后大家心里都服气，这才算数。",
    avatar: "assets/portraits/li_jiusong/Screenshot%202026-05-07%20204725.png",
  },
  neng_niang: {
    name: "嫩娘",
    text: "有些话轻轻讲也听得进。人心软下来，家里厢的灯就亮起来了。",
    avatar: "assets/portraits/neng_niang/Screenshot%202026-05-07%20204824.png",
  },
  zhu_zhen: {
    name: "朱桢",
    text: "这场面我熟啊，先别急着下结论。给我三句话，保证把气氛接回来。",
    avatar: "assets/portraits/zhu_zhen/Screenshot%202026-05-07%20204853.png",
  },
};

const cards = document.querySelectorAll(".character-card");
const dialogueName = document.getElementById("dialogue-name");
const dialogueText = document.getElementById("dialogue-text");
const dialogueAvatar = document.getElementById("dialogue-avatar");

function selectCharacter(card) {
  const key = card.dataset.character;
  const character = characters[key];

  if (!character) return;

  dialogueName.textContent = character.name;
  dialogueText.textContent = character.text;
  dialogueAvatar.style.backgroundImage = `url("${character.avatar}")`;
  dialogueAvatar.classList.add("is-active");

  cards.forEach((item) => {
    item.classList.remove("is-selected");
    item.setAttribute("aria-pressed", "false");
  });
  card.classList.add("is-selected");
  card.setAttribute("aria-pressed", "true");
}

cards.forEach((card, index) => {
  card.addEventListener("click", () => selectCharacter(card));

  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      selectCharacter(card);
    }
  });

  card.setAttribute("tabindex", "0");
  card.setAttribute("role", "button");
  card.setAttribute("aria-pressed", "false");

  if (index === 0) {
    selectCharacter(card);
  }
});
