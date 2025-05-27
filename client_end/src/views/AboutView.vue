<template>
  <div class="txt">
    <div
      class="p-6 bg-[#121212] h-screen flex flex-col items-center justify-center space-y-6 flex;"
    >
      <div v-for="(item, index) in reflections" :key="index">
        <h3 class="txt-header">{{ item.name }}</h3>
        <p class="txt-line">
          {{ item.message }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TeamReflection",
  data() {
    return {
      reflections: [
        {
          name: "Theo",
          message: "If I got another go, I’d definitely pick .Net." + "" + "",
        },
        {
          name: "James",
          message:
            "Honestly, getting the Django APIs humming was pretty satisfying. Wrestling with SSL certs in NGINX was a fun challenge, and spinning up Node.js services felt like flexing my DevOps muscles. I’m glad the README made sense for everyone." +
            "" +
            "",
        },
        {
          name: "Winter",
          message:
            "Writing those cheeky weather alerts and button tips was my jam. I sketched up flowcharts and logic diagrams to keep our ideas straight, then knocked out all the paperwork for project docs. Seeing it all pop on screen was pretty sweet.",
        },
      ],
    };
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");

* {
  font-family: "Roboto", sans-serif;
}

.neon-glow {
  color: #00ffff;
  text-shadow: 0 0 8px #00ffff, 0 0 16px #00ffff;
}

.neon-glow-p {
  text-shadow: 0 0 3px #00ffff, 0 0 6px #00ffff;
}

.txt {
  margin-top: 100px;
}

.txt-line {
  font-size: 1.2rem;
  color: #00ffe1;
  text-shadow: 0 0 3px #00ffe1;
  font-weight: 400;
  line-height: 2rem;
  text-align: center;
}

.txt-header {
  font-size: 2rem;
  color: #00ffff;
  text-shadow: 0 0 2px #00ffff, 0 0 8px #00ffff, 0 0 16px #00ffff,
    0 0 32px rgba(0, 255, 255, 0.5);
  font-weight: 400;
  line-height: 2rem;
  text-align: center;
}
</style>
