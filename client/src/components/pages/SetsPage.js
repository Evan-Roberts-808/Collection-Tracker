import React, { useState, useEffect } from 'react'
import Container from "react-bootstrap/Container"
import Sets from "../Sets.js"

function SetsPage() {

  // Define state variables for each category
  const [promoSets, setPromoSets] = useState([]);
  const [starterDeckSets, setStarterDeckSets] = useState([]);
  const [regularSets, setRegularSets] = useState([]);

  // Fetch the data and categorize the sets
  useEffect(() => {
    fetch('/sets')
      .then((response) => response.json())
      .then((data) => {
        // Filter the sets based on their category
        const promoSets = data.filter((set) => set.name.includes('Promo'));
        const starterDeckSets = data.filter((set) => set.name.includes('Starter Deck'));
        const regularSets = data.filter((set) => !set.name.includes('Promo') && !set.name.includes('Starter Deck'));

        // Update the state variables with the categorized sets
        setPromoSets(promoSets);
        setStarterDeckSets(starterDeckSets);
        setRegularSets(regularSets);
      });
  }, []);

  return (
    <Container>
      <h2>Sets</h2>
      <Sets data={regularSets}/>
      <h2>Promos</h2>
      <Sets data={promoSets}/>
      <h2>Starter Decks</h2>
      <Sets data={starterDeckSets}/>
    </Container>
  )
}

export default SetsPage