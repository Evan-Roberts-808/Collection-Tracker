import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import Container from 'react-bootstrap/Container'
import {Card, Row, Col, Button} from 'react-bootstrap'
import Table from 'react-bootstrap/Table'
import Modal from 'react-bootstrap/Modal'

function SetsDetailsPage() {

  const { id } = useParams()
  const [details, setDetails] = useState([])
  const [showModal, setShowModal] = useState(false);
  const [selectedCard, setSelectedCard] = useState(null);
  const numberOfCards = details.cards ? details.cards.length : 0;

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
      <Card className="text-white col-sm-2 tcg-cards" onClick={() => handleCardClick(card)}>
        <Card.Img src={card.image_url} alt={card.name} className="card-image" />
        <Card.ImgOverlay className="card-overlay">
          <div className="card-info">
            <Card.Text className="card-info-text">{card.name} | {card.position}</Card.Text>
          </div>
        </Card.ImgOverlay>
      </Card>
    );
  });
  
  const handleCardClick = (card) => {
    setSelectedCard(card);
    setShowModal(true);
  };  

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedCard(null);
  };

  return (
    <Container>
<article>
      <Row>
        <Col md={6}>
          <h2>{details.name}</h2>
          <p>{details.description}</p>
        </Col>
        <Col md={6}>
          <Table className="total-cards">
            <thead>
              <tr>
                <th>Total Cards</th>
                <th>Your Cards</th>
                <th>Completion</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{numberOfCards}</td>
                <td>#</td>
                <td>%</td>
              </tr>
            </tbody>
          </Table>
        </Col>
      </Row>
    </article>
    <hr />
    <section className='row justify-content-center'>
      {cardsDisplay}
    </section>

    {/* Modal */}
    <Modal show={showModal} onHide={handleCloseModal}>
      <Modal.Header closeButton>
        <Modal.Title>Card Details</Modal.Title>
      </Modal.Header>
      <Modal.Body>
  {selectedCard && (
    <Row>
      <Col md={6}>
        <img className="modal-img" src={selectedCard.image_url} alt={selectedCard.name} />
      </Col>
      <Col md={6}>
        <div>
          <h4>{selectedCard.name}</h4>
          <p><b>Effect:</b> {selectedCard.description}</p>
          {selectedCard.element && <p><b>Element:</b> {selectedCard.element}</p>}
          {selectedCard.rune_type && <p><b>Rune Type:</b> {selectedCard.rune_type}</p>}
          {selectedCard.subclass1 && selectedCard.subclass2 && (
            <p>
              <b>Subclasses:</b> {selectedCard.subclass1} / {selectedCard.subclass2}
            </p>
          )}
          {selectedCard.attack_defense && (
            <p><b>Attack | Defense:</b> {selectedCard.attack_defense}</p>
          )}
          <p><b>Set Position:</b> {selectedCard.position}</p>
          <p><b>Rarity:</b> {selectedCard.rarity}</p>
        </div>
      </Col>
    </Row>
  )}
</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleCloseModal}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>

    </Container>
  )
}

export default SetsDetailsPage