const cardContainer = document.querySelector('.react-card');

// React component for form inputs
class CardInput extends React.Component {
  render() {
    return /*#__PURE__*/(
      React.createElement("fieldset", null, /*#__PURE__*/
      React.createElement("input", { name: this.props.name, id: this.props.id, type: this.props.type, min:this.props.min, value:this.props.value || 'text', placeholder: this.props.placeholder, required: true })));


  }}


// React component for textarea
class CardTextarea extends React.Component {
  render() {
    return /*#__PURE__*/(
      React.createElement("fieldset", null, /*#__PURE__*/
      React.createElement("textarea", { name: this.props.name, id: this.props.id, placeholder: this.props.placeholder, required: true })));


  }}


// React component for form button
class CardBtn extends React.Component {
  render() {
    return /*#__PURE__*/(
      React.createElement("fieldset", null, /*#__PURE__*/
      React.createElement("button", { className: this.props.className, type: this.props.type, value: this.props.value }, this.props.value)));


  }}


// React component for social profile links
class CardProfileLinks extends React.Component {
  render() {
    const profileLinks = ['twitter', 'linkedin', 'dribbble', 'facebook'];

    const linksList = profileLinks.map((link, index) => /*#__PURE__*/
    React.createElement("li", { key: index }, /*#__PURE__*/React.createElement("a", { href: "#" }, /*#__PURE__*/React.createElement("i", { className: 'fa fa-' + link }))));


    return /*#__PURE__*/(
      React.createElement("div", { className: "card-social-links" }, /*#__PURE__*/
      React.createElement("ul", { className: "social-links" },
      linksList)));



  }}


// React component for the front side of the card
class CardFront extends React.Component {
  render() {
    return /*#__PURE__*/(
      React.createElement("div", { className: "card-side side-front" }, /*#__PURE__*/
      React.createElement("div", { className: "container-fluid" }, /*#__PURE__*/
      React.createElement("div", { className: "row" }, /*#__PURE__*/
      React.createElement("div", { className: "col-xs-6" }, /*#__PURE__*/
      React.createElement("img", { src: "https://source.unsplash.com/w8YICpz1I10/358x458" })), /*#__PURE__*/


      React.createElement("div", { className: "col-xs-6 side-front-content" }, /*#__PURE__*/
      React.createElement("h2", null, "Czech based"), /*#__PURE__*/

      React.createElement("h1", null, "UI/UX Designer"), /*#__PURE__*/

      React.createElement("p", null, "Andrey is driven by turning ideas into scalable and and empowering experiences that solve real life problems."), /*#__PURE__*/

      React.createElement("p", null, "He is currently the founder of Dvorak Media. Previously, Andrey was a product designer at Dropbox."), /*#__PURE__*/

      React.createElement("p", null, "Over the years, Michael has been priviledged to have worked with Adobe, Evernote, Square and more."))))));





  }}


// React component for the back side of the card
class CardBack extends React.Component {
  render() {
    return /*#__PURE__*/(
      React.createElement("div", { className: "card-side side-back" }, /*#__PURE__*/
      React.createElement("div", { className: "container-fluid" }, /*#__PURE__*/
      React.createElement("h1", null, "Search Movie To Predict"), /*#__PURE__*/

      React.createElement("form", { formAction: "", className: "card-form" }, /*#__PURE__*/
      React.createElement("div", { className: "row" }, /*#__PURE__*/
      React.createElement("div", { className: "col-xs-6" }, /*#__PURE__*/
      React.createElement(CardInput, { name: "release_year", id: "release_year", type: "number", min:1980, value:1980 })), /*#__PURE__*/


      React.createElement("div", { className: "col-xs-6" }, /*#__PURE__*/
      React.createElement(CardInput, { name: "contactLastName", id: "contactLastName", type: "text", placeholder: "Your last name" }))), /*#__PURE__*/



      React.createElement("div", { className: "row" }, /*#__PURE__*/
      React.createElement("div", { className: "col-xs-6" }, /*#__PURE__*/
      React.createElement(CardInput, { name: "contactEmail", id: "contactEmail", type: "email", placeholder: "Your email address" })), /*#__PURE__*/


      React.createElement("div", { className: "col-xs-6" }, /*#__PURE__*/
      React.createElement(CardInput, { name: "contactSubject", id: "contactSubject", type: "text", placeholder: "Subject" }))), /*#__PURE__*/



      React.createElement(CardTextarea, { name: "contactMessage", id: "contactMessage", placeholder: "Your message" }), /*#__PURE__*/

      React.createElement(CardBtn, { className: "btn btn-primary", type: "submit", value: "Send message" })), /*#__PURE__*/


      )));



  }}


// React component for the card (main component)
class Card extends React.Component {
  render() {
    return /*#__PURE__*/(
      React.createElement("div", { className: "card-container" }, /*#__PURE__*/
      React.createElement("div", { className: "card-body" }, /*#__PURE__*/
      React.createElement(CardBack, null), /*#__PURE__*/
      React.createElement(CardFront, null))));
  }}


// Render Card component
ReactDOM.render( /*#__PURE__*/React.createElement(Card, null), cardContainer);