<template>
  <div class="container">
    <button @pointerdown="startSpeech"></button>
    <h1>{{ recognized }}</h1>
  </div>
</template>

<script>
import io from "socket.io-client";
let SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

export default {
  name: "Home",
  props: {
    msg: String,
  },
  mounted() {
    this.socket.on("message", (data) => {
      //const enc = new TextDecoder("utf-8");
      console.log(data);
    });
    console.log(this.recognition);
    if (this.recognition) {
        this.recognized = 'aanwezig';
      this.recognition.continuous = false;
      this.recognition.lang = "nl-BE";
      this.recognition.interimResults = false;
      this.recognition.maxAlternatives = 1;
      this.recognition.start();
      this.recognition.addEventListener("result", (evt) => {
          //this.recognized = 'resultaat';
          console.log(evt);
        this.recognized = evt.results[0][0].transcript;
        this.translate();
        //this.recognition.start();
      });
    }
  },
  data() {
    return {
      //lastvalue: 0,
      socket: io("http://localhost:3000/"),
      recognition: SpeechRecognition ? new window.webkitSpeechRecognition() : false,
      recognized: "",
    };
  },
  methods: {
    translate() {
      let topic;
      if (
        this.recognized.includes("rood") ||
        this.recognized.includes("rode")
      ) {
        topic = "led/red";
      }
      if (
        this.recognized.includes("blauw") ||
        this.recognized.includes("blauwe")
      ) {
        topic = "led/blue";
      }

      let state;
      if (this.recognized.includes("aan")) {
        state = "on";
      }
      if (this.recognized.includes("uit")) {
        state = "off";
      }

      if (topic !== "" && state !== "") {
        this.socket.emit("message", { topic: topic, message: state });
      }
      //console.log("function executed");
      //
    },
    startSpeech() {
      this.recognition.start();
      this.recognized = "aan het luisteren";
      //console.log('down');
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.container{
    height: 100%;
    display: flex;
    flex-flow: column;
    align-items: center;
    justify-content: center;
}
button {
  border-radius: 50%;
  width: 200px;
  height: 200px;
  border: none;
  color: white;
  font-family: Avenir, Arial, sans-serif;
  font-weight: 900;
  font-size: 2.5rem;
  background: red;
  text-shadow: 0 3px 1px rgba(122, 17, 8, 0.8);
  box-shadow: 0 8px 0 rgb(183, 9, 0), 0 15px 20px rgba(0, 0, 0, 0.35);
  text-transform: uppercase;
  transition: 0.4s all ease-in;
  outline: none;
  cursor: pointer;
  text-align: center;
  -webkit-user-select: none;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

button:active {
  padding-top: 3px;
  transform: translateY(4px);
  box-shadow: 0 4px 0 rgb(183, 0, 0), 0 8px 6px rgba(0, 0, 0, 0.45);
}
</style>
