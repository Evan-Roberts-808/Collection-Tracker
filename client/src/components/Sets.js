import React from 'react'
import Card from "react-bootstrap/Card";
import { Link } from "react-router-dom"

function Sets({data}) {
  const sets = data.map((data) => {
    const url = `/sets/${data.id}`;
    return (
      <Card className='col-sm-3 offset-sm-1' key={data.id}>
      <Link to={url} style={{textDecoration: 'none'}}>
        <Card.Img variant='top' src={data.icon_url}/>
        <Card.Body>
          <Card.Title>{data.name}</Card.Title>
          <Card.Text>{data.description}</Card.Text>
        </Card.Body>
        </Link>
      </Card>
    )
  })

  return <div className="row justify-content-center">{sets}</div>
}

export default Sets