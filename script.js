const characters = {
  ade: {
    name: "阿德哥",
    text: "我在老娘舅一待就是二十年啦，见过的故事多得像锅里的葱油面。慢慢吃，生活总会有好味道。",
    avatar:
      "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=420&q=80",
  },
  aqing: {
    name: "阿庆",
    text: "客人一笑，心里就亮堂。等会儿给你加碗秘制浇头，带你尝尝我们店里的活泼劲儿！",
    avatar:
      "https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=420&q=80",
  },
};

const cards = document.querySelectorAll(".character-card");
const dialogueName = document.getElementById("dialogue-name");
const dialogueText = document.getElementById("dialogue-text");
const dialogueAvatar = document.getElementById("dialogue-avatar");

cards.forEach((card) => {
  card.addEventListener("click", () => {
    const key = card.dataset.character;
    const character = characters[key];

    if (!character) return;

    dialogueName.textContent = character.name;
    dialogueText.textContent = character.text;
    dialogueAvatar.style.backgroundImage = `url(${character.avatar})`;
    dialogueAvatar.classList.add("is-active");

    cards.forEach((item) => item.classList.remove("is-selected"));
    card.classList.add("is-selected");
  });

  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      card.click();
    }
  });

  card.setAttribute("tabindex", "0");
});
