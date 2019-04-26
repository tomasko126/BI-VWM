<?php

namespace App\Model;

use Nette;

class BaseDocumentsModel {
    private $indexedArticlesFile = "../../analyzed/_indexedArticles.json";

    public function getAllStoredDocuments() {

        // Open up file with key/value pairs of docId - docName
        $file = fopen($this->indexedArticlesFile, "r");
        $result = fread($file, filesize($this->indexedArticlesFile));

        $result = json_decode($result, true);

        return $result;
    }

    public function getOneRandomDocument() {
        $allDocs = $this->getAllStoredDocuments();

        $randomDocIndex = rand(1, count((array) $allDocs));

        return $randomDocIndex;
    }

    public function getDocument($id) {
        $allDocs = $this->getAllStoredDocuments();
        $docToOpen = $allDocs[$id];

        $file = fopen("../../plain_articles/" . $docToOpen, "r");
        $result = fread($file, filesize("../../plain_articles/" . $docToOpen));

        $docObject = array();
        $docObject['id'] = $id;
        $docObject['name'] = $this->getDocumentName($id);
        $docObject['content'] = $result;

        return $docObject;
    }

    public function getDocumentName($id) {
        return $this->getAllStoredDocuments()[$id];
    }
}