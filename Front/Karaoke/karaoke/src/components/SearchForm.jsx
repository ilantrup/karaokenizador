import { useState } from "react"

import { VideoComponent } from './VideoComponent.jsx'



export const SearchForm = () => {

  const [query, setQuery] = useState('')
  const [songName, setSongName] = useState('')

  
  const handleSubmit = (event) => {
    event.preventDefault()
    const valorInput = query
    console.log('Valor del input:', valorInput)
    setSongName(valorInput)
    setQuery('')
    event.target.value = ''
  }

  const handleChange = (event) => {
    setQuery(event.target.value)
  }

  return (
    <div>
    <form className='search' onSubmit={handleSubmit}>
      <label className='search-label' htmlFor="songName">Enter song name: </label>
      <input onChange={handleChange} type="text" value={query} id="songName" placeholder="Song..." />
      <button type="submit">Search</button>
    </form>
    <VideoComponent 
    title={songName}/>
  </div>
  )
}