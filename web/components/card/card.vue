<template>
<div class="container" v-bind:style="{ width: + size * 180 + 'px'}">

    <div class = "text-block">
        <div class="middle-text">{{number}}</div>
        <div class="bottom-text">{{description}} </div>
        <div class="middle-text2" :style="{color: color}"><span>{{description2}} </span></div>
    </div>
    <img class="image" :src="require(`~/assets/img/${path}`)" v-if="path"/>  
    
</div>

</template>

<script src="./card.js" ></script>

<style src="./card.css"></style>