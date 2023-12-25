/* eslint-disable react/prop-types */
import { useEffect, useState, useMemo } from 'react'
import ReactPlayer from 'react-player'
import {getVideo} from '../functions/karoke_functions.js'
import {LoadingSpinner} from './LoadingSpinner.jsx'

export const VideoComponent = ({ title='' }) => {
    const [video, setVideo] = useState('')
    const [loading, setLoading] = useState(false)
    const lastSearchedTitle = useMemo(() => {
      console.log("entre al useMemo con el valor: " + title)
      return {title}
    }, [title])

    useEffect(() => {
      if (lastSearchedTitle !== title) {
        const fetchData = async () => {
          console.log("entre")
          setLoading(true)
          const url = await getVideo(title)
          setVideo(url)
          setLoading(false)
        }
        fetchData()
      }
    }, [lastSearchedTitle, title])

    return (
        <div>
            {
                loading 
                ? <LoadingSpinner />
                :<ReactPlayer className='player' 
                    url={video}
                    width='100%'
                    height='100%'
                    controls
                  />  
            }
      
      </div>
    )
}

