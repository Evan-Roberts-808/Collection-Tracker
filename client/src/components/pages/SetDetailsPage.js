import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import Container from 'react-bootstrap/Container'
import Card from 'react-bootstrap/Card'

function SetsDetailsPage() {

  const { id } = useParams()
  const [details, setDetails] = useState([])
  
  useEffect(() => {
    fetch(`/sets/${id}`)
      .then((response) => response.json())
      .then((data) => setDetails(data))
  }, [id])

  if (Object.keys(details).length === 0) {
    return null;
  }

  const cardsDisplay = details.cards.map((card) => {
    return (
    <Card className="text-white col-sm-2">
      <Card.Img src={card.image_url} />
      <Card.ImgOverlay>
        <Card.Title>{card.name}</Card.Title>
        <Card.Text>{card.position}</Card.Text>
      </Card.ImgOverlay>
    </Card>
    )
  })

  return (
    <Container className='row'>
      {cardsDisplay}
    </Container>
  )
}

export default SetsDetailsPage