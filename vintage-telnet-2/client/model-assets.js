// Optional visual assets. Gameplay and the map never depend on these files.
export async function loadSpeciesModel(id){
 if(!['humano','felaryn','dravak','marevyn','vesperi'].includes(id))throw new Error('No hay modelo disponible.');
 const {GLTFLoader}=await import('./vendor/GLTFLoader.js');
 const result=await new GLTFLoader().loadAsync(`/client/models/species/${id}.glb`);
 return result.scene;
}
export function disposeModel(root){
 const geometries=new Set(),materials=new Set(),textures=new Set();
 root.traverse(object=>{if(object.geometry)geometries.add(object.geometry);for(const material of object.material?(Array.isArray(object.material)?object.material:[object.material]):[]){materials.add(material);for(const value of Object.values(material))if(value?.isTexture)textures.add(value);}});
 for(const texture of textures){texture.dispose();if(typeof texture.image?.close==='function')texture.image.close();}
 for(const material of materials)material.dispose();
 for(const geometry of geometries)geometry.dispose();
}
