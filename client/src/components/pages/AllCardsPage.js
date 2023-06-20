import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Pagination from 'react-bootstrap/Pagination';
import {Modal, Row, Col, Button} from 'react-bootstrap'

function AllCardsPage() {
  const [cards, setCards] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [showModal, setShowModal] = useState(false);
  const [selectedCard, setSelectedCard] = useState(null);
  const cardsPerRow = 6;
  const rowsPerPage = 4;
  const pageLimit = 2; // Number of page numbers to display on each side of the current page

  useEffect(() => {
    fetch('/cards')
      .then((response) => response.json())
      .then((data) => setCards(data));
  }, []);

  const cardsPerPage = cardsPerRow * rowsPerPage;
  const indexOfLastCard = currentPage * cardsPerPage;
  const indexOfFirstCard = indexOfLastCard - cardsPerPage;
  const currentCards = cards.slice(indexOfFirstCard, indexOfLastCard);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const totalPages = Math.ceil(cards.length / cardsPerPage);
  const pageNumbers = [];

  const cardsDisplay = currentCards.map((card) => { // Display only the cards for the current page
    return (
      <Card className="text-white col-sm-2 tcg-cards" key={card.id} onClick={() => handleCardClick(card)}>
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

  if (totalPages <= 1) {
    // No need to display pagination if there is only one page
    return (
      <Container>
        <section className="row">{cardsDisplay}</section>
      </Container>
    );
  }

  if (currentPage <= pageLimit + 1) {
    for (let i = 1; i <= Math.min(totalPages, pageLimit * 2 + 1); i++) {
      pageNumbers.push(
        <Pagination.Item
          key={i}
          active={i === currentPage}
          onClick={() => handlePageChange(i)}
        >
          {i}
        </Pagination.Item>
      );
    }
    if (totalPages > pageLimit * 2 + 1) {
      pageNumbers.push(<Pagination.Ellipsis key="ellipsis1" />);
      pageNumbers.push(
        <Pagination.Item
          key={totalPages}
          active={totalPages === currentPage}
          onClick={() => handlePageChange(totalPages)}
        >
          {totalPages}
        </Pagination.Item>
      );
    }
  } else if (currentPage >= totalPages - pageLimit) {
    pageNumbers.push(
      <Pagination.Item
        key={1}
        active={1 === currentPage}
        onClick={() => handlePageChange(1)}
      >
        {1}
      </Pagination.Item>
    );
    if (totalPages > pageLimit * 2 + 1) {
      pageNumbers.push(<Pagination.Ellipsis key="ellipsis1" />);
    }
    for (let i = Math.max(1, totalPages - pageLimit * 2); i <= totalPages; i++) {
      pageNumbers.push(
        <Pagination.Item
          key={i}
          active={i === currentPage}
          onClick={() => handlePageChange(i)}
        >
          {i}
        </Pagination.Item>
      );
    }
  } else {
    pageNumbers.push(
      <Pagination.Item
        key={1}
        active={1 === currentPage}
        onClick={() => handlePageChange(1)}
      >
        {1}
      </Pagination.Item>
    );
    if (totalPages > pageLimit * 2 + 1) {
      pageNumbers.push(<Pagination.Ellipsis key="ellipsis1" />);
    }
    for (
      let i = currentPage - pageLimit;
      i <= currentPage + pageLimit;
      i++
    ) {
      pageNumbers.push(
        <Pagination.Item
          key={i}
          active={i === currentPage}
          onClick={() => handlePageChange(i)}
        >
          {i}
        </Pagination.Item>
      );
    }
    if (totalPages > pageLimit * 2 + 1) {
      pageNumbers.push(<Pagination.Ellipsis key="ellipsis2" />);
      pageNumbers.push(
        <Pagination.Item
          key={totalPages}
          active={totalPages === currentPage}
          onClick={() => handlePageChange(totalPages)}
        >
          {totalPages}
        </Pagination.Item>
      );
    }
  }

  return (
    <Container>
      <section className="row">{cardsDisplay}</section>
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
      <Pagination>
        <Pagination.First
          onClick={() => handlePageChange(1)}
          disabled={currentPage === 1}
        />
        <Pagination.Prev
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        />
        {pageNumbers}
        <Pagination.Next
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        />
        <Pagination.Last
          onClick={() => handlePageChange(totalPages)}
          disabled={currentPage === totalPages}
        />
      </Pagination>
    </Container>
  );
}

export default AllCardsPage;
