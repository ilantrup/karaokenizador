import axios from 'axios'

export const getVideo = async (title) => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/get-video/?title=${title}`, {
            responseType: 'blob', // Importante para manejar archivos binarios
        })
        console.log(URL.createObjectURL(new Blob([response.data], { type: 'video/mp4' })))
        const videoBlob = new Blob([response.data], { type: 'video/mp4' })
        const url = URL.createObjectURL(videoBlob)
        return url
    } catch (error) {
        console.error('Error al obtener el video:', error)
    }
  }