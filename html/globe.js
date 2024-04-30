import * as THREE from '//unpkg.com/three/build/three.module.js';
//Dark-mode checker 
const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

// Define variables based on mode
let modeVariable;

if (prefersDarkMode) {
// Assign value for dark mode
modeVariable = '#151515';
} else {
// Assign value for light mode
modeVariable = '#FFFFFF';
}

const world = Globe({ animateIn: false })
  (document.getElementById('globe'))
  .width(360)
  .height(360)
  .backgroundColor(modeVariable)
  .pointOfView({ lat: 0, lng: 0, altitude: 1.7 })
  .globeImageUrl('./earth-blue-marble.jpg')
  .bumpImageUrl('./earth-topology.png');

// Auto-rotate
world.controls().autoRotate = true;
world.controls().autoRotateSpeed = 0.35;


// Add clouds sphere
const CLOUDS_IMG_URL = './clouds.png'; // from https://github.com/turban/webgl-earth
const CLOUDS_ALT = 0.002;
const CLOUDS_ROTATION_SPEED = -0.006; // deg/frame

new THREE.TextureLoader().load(CLOUDS_IMG_URL, cloudsTexture => {
  const clouds = new THREE.Mesh(
    new THREE.SphereGeometry(world.getGlobeRadius() * (1 + CLOUDS_ALT), 75, 75),
    new THREE.MeshPhongMaterial({ map: cloudsTexture, transparent: true })
  );
  world.scene().add(clouds);

  (function rotateClouds() {
    clouds.rotation.y += CLOUDS_ROTATION_SPEED * Math.PI / 180;
    requestAnimationFrame(rotateClouds);
  })();
});