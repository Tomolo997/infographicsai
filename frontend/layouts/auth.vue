<template>
  <div class="flex flex-col md:flex-row h-screen">
    
    <div class="w-full md:w-1/2 flex items-center justify-center">
      <slot />
    </div>
    <div class="w-full md:w-1/2 hidden md:flex bg-indigo-500 items-center justify-center">
      <div class="text-white text-center">
        <div class="text-white flex items-center justify-center gap-6 text-3xl font-bold">
          
          <NuxtImg class="w-[64px]" src="../public/images/logo.svg" alt="logo" />
          <h1 class="text-white font-base text-4xl">
            Ainfographic
          </h1>
        </div>
      </div>
    </div>
  </div>
 
</template>
